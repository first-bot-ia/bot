"""
Implementación PostgreSQL del repositorio de clientes
"""
import psycopg2
from psycopg2.extras import RealDictCursor
from typing import List, Optional
import os

from domain.entities.client import Client
from domain.repositories.client_repository import ClientRepository


class PostgreSQLClientRepository(ClientRepository):
    """
    Implementación PostgreSQL del repositorio de clientes
    """
    
    def __init__(self, database_url: str):
        self.database_url = database_url
        self._ensure_table_exists()
    
    def _get_connection(self):
        """Obtiene conexión a PostgreSQL"""
        return psycopg2.connect(self.database_url)
    
    def _ensure_table_exists(self):
        """Asegura que la tabla clientes existe"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS clientes (
                    id SERIAL PRIMARY KEY,
                    nombre VARCHAR(255) NOT NULL,
                    telefono VARCHAR(50) NOT NULL UNIQUE,
                    email VARCHAR(255),
                    activo BOOLEAN DEFAULT true,
                    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    ultimo_envio TIMESTAMP,
                    total_enviados INTEGER DEFAULT 0
                )
            ''')
            
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Error creando tabla clientes: {e}")
    
    def save(self, client: Client) -> Client:
        """Guarda un cliente en PostgreSQL"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        try:
            if client.id is None:
                # Nuevo cliente
                cursor.execute("""
                    INSERT INTO clientes (nombre, telefono, email, activo, fecha_registro, total_enviados)
                    VALUES (%s, %s, %s, %s, %s, %s) 
                    RETURNING id
                """, (
                    client.nombre,
                    client.telefono, 
                    client.email,
                    client.activo,
                    client.fecha_registro,
                    client.total_enviados
                ))
                
                result = cursor.fetchone()
                if not result:
                    raise ValueError("Error insertando cliente")
                client_id = result[0]
                conn.commit()
                
                # Retornar cliente con ID asignado
                return Client(
                    id=client_id,
                    nombre=client.nombre,
                    telefono=client.telefono,
                    email=client.email,
                    activo=client.activo,
                    fecha_registro=client.fecha_registro,
                    ultimo_envio=client.ultimo_envio,
                    total_enviados=client.total_enviados
                )
            else:
                # Actualizar cliente existente
                cursor.execute("""
                    UPDATE clientes 
                    SET nombre=%s, telefono=%s, email=%s, activo=%s, 
                        ultimo_envio=%s, total_enviados=%s
                    WHERE id=%s
                """, (
                    client.nombre,
                    client.telefono,
                    client.email, 
                    client.activo,
                    client.ultimo_envio,
                    client.total_enviados,
                    client.id
                ))
                
                conn.commit()
                return client
                
        except psycopg2.IntegrityError:
            conn.rollback()
            raise ValueError(f"Cliente con teléfono {client.telefono} ya existe")
        finally:
            conn.close()
    
    def find_by_id(self, client_id: int) -> Optional[Client]:
        """Busca cliente por ID"""
        conn = self._get_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        try:
            cursor.execute("SELECT * FROM clientes WHERE id = %s", (client_id,))
            row = cursor.fetchone()
            
            if row:
                return self._row_to_client(row)
            return None
            
        finally:
            conn.close()
    
    def find_by_phone(self, phone: str) -> Optional[Client]:
        """Busca cliente por teléfono"""
        conn = self._get_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        try:
            cursor.execute("SELECT * FROM clientes WHERE telefono = %s", (phone,))
            row = cursor.fetchone()
            
            if row:
                return self._row_to_client(row)
            return None
            
        finally:
            conn.close()
    
    def find_all_active(self) -> List[Client]:
        """Obtiene todos los clientes activos"""
        conn = self._get_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        try:
            cursor.execute("SELECT * FROM clientes WHERE activo = true ORDER BY nombre")
            rows = cursor.fetchall()
            
            return [self._row_to_client(row) for row in rows]
            
        finally:
            conn.close()
    
    def find_all(self) -> List[Client]:
        """Obtiene todos los clientes"""
        conn = self._get_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        try:
            cursor.execute("SELECT * FROM clientes ORDER BY nombre")
            rows = cursor.fetchall()
            
            return [self._row_to_client(row) for row in rows]
            
        finally:
            conn.close()
    
    def update(self, client: Client) -> Client:
        """Actualiza cliente existente"""
        if client.id is None:
            raise ValueError("No se puede actualizar cliente sin ID")
        
        return self.save(client)
    
    def delete(self, client_id: int) -> bool:
        """Elimina cliente"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("DELETE FROM clientes WHERE id = %s", (client_id,))
            deleted = cursor.rowcount > 0
            conn.commit()
            return deleted
            
        finally:
            conn.close()
    
    def count_active(self) -> int:
        """Cuenta clientes activos"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("SELECT COUNT(*) FROM clientes WHERE activo = true")
            result = cursor.fetchone()
            count = result[0] if result else 0
            return count
            
        finally:
            conn.close()
    
    def _row_to_client(self, row: dict) -> Client:
        """Convierte fila de BD a entidad Client"""
        return Client(
            id=row['id'],
            nombre=row['nombre'],
            telefono=row['telefono'],
            email=row['email'],
            activo=row['activo'],
            fecha_registro=row['fecha_registro'],
            ultimo_envio=row['ultimo_envio'],
            total_enviados=row['total_enviados'] or 0
        ) 