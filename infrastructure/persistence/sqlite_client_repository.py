"""
Implementación SQLite del repositorio de clientes (fallback)
"""
import sqlite3
from typing import List, Optional
from pathlib import Path

from domain.entities.client import Client
from domain.repositories.client_repository import ClientRepository


class SQLiteClientRepository(ClientRepository):
    """
    Implementación SQLite del repositorio de clientes
    """
    
    def __init__(self, db_path: str = "clientes_spam.db"):
        self.db_path = db_path
        self._ensure_table_exists()
    
    def _get_connection(self):
        """Obtiene conexión a SQLite"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Para acceso por nombre de columna
        return conn
    
    def _ensure_table_exists(self):
        """Asegura que la tabla clientes existe"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS clientes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    telefono TEXT NOT NULL UNIQUE,
                    email TEXT,
                    activo BOOLEAN DEFAULT 1,
                    fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP,
                    ultimo_envio DATETIME,
                    total_enviados INTEGER DEFAULT 0
                )
            ''')
            
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"⚠️ Error creando tabla clientes: {e}")
    
    def save(self, client: Client) -> Client:
        """Guarda un cliente en SQLite"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        try:
            if client.id is None:
                # Nuevo cliente
                cursor.execute("""
                    INSERT INTO clientes (nombre, telefono, email, activo, fecha_registro, total_enviados)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    client.nombre,
                    client.telefono,
                    client.email,
                    client.activo,
                    client.fecha_registro.isoformat() if client.fecha_registro else None,
                    client.total_enviados
                ))
                
                client_id = cursor.lastrowid
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
                    SET nombre=?, telefono=?, email=?, activo=?, 
                        ultimo_envio=?, total_enviados=?
                    WHERE id=?
                """, (
                    client.nombre,
                    client.telefono,
                    client.email,
                    client.activo,
                    client.ultimo_envio.isoformat() if client.ultimo_envio else None,
                    client.total_enviados,
                    client.id
                ))
                
                conn.commit()
                return client
                
        except sqlite3.IntegrityError:
            conn.rollback()
            raise ValueError(f"Cliente con teléfono {client.telefono} ya existe")
        finally:
            conn.close()
    
    def find_by_id(self, client_id: int) -> Optional[Client]:
        """Busca cliente por ID"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("SELECT * FROM clientes WHERE id = ?", (client_id,))
            row = cursor.fetchone()
            
            if row:
                return self._row_to_client(row)
            return None
            
        finally:
            conn.close()
    
    def find_by_phone(self, phone: str) -> Optional[Client]:
        """Busca cliente por teléfono"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("SELECT * FROM clientes WHERE telefono = ?", (phone,))
            row = cursor.fetchone()
            
            if row:
                return self._row_to_client(row)
            return None
            
        finally:
            conn.close()
    
    def find_all_active(self) -> List[Client]:
        """Obtiene todos los clientes activos"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("SELECT * FROM clientes WHERE activo = 1 ORDER BY nombre")
            rows = cursor.fetchall()
            
            return [self._row_to_client(row) for row in rows]
            
        finally:
            conn.close()
    
    def find_all(self) -> List[Client]:
        """Obtiene todos los clientes"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
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
            cursor.execute("DELETE FROM clientes WHERE id = ?", (client_id,))
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
            cursor.execute("SELECT COUNT(*) FROM clientes WHERE activo = 1")
            result = cursor.fetchone()
            count = result[0] if result else 0
            return count
            
        finally:
            conn.close()
    
    def _row_to_client(self, row) -> Client:
        """Convierte fila de BD a entidad Client"""
        from datetime import datetime
        
        # Convertir fechas string a datetime si es necesario
        fecha_registro = None
        if row['fecha_registro']:
            try:
                fecha_registro = datetime.fromisoformat(row['fecha_registro'])
            except:
                fecha_registro = None
        
        ultimo_envio = None
        if row['ultimo_envio']:
            try:
                ultimo_envio = datetime.fromisoformat(row['ultimo_envio'])
            except:
                ultimo_envio = None
        
        return Client(
            id=row['id'],
            nombre=row['nombre'],
            telefono=row['telefono'],
            email=row['email'],
            activo=bool(row['activo']),
            fecha_registro=fecha_registro,
            ultimo_envio=ultimo_envio,
            total_enviados=row['total_enviados'] or 0
        ) 