import sqlite3


class PartidoPoliticoDB:
    def __init__(self, db_path, partido, miembros, nro_mesa):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.nro_mesa = nro_mesa
        self.partido = partido
        self.miembros = miembros

    def mesa_exists(self):
        try:
            select_query = f"""
                SELECT 1 FROM "{self.partido}" WHERE nro_mesa = ?;
            """
            self.cursor.execute(select_query, (self.nro_mesa,))
            result = self.cursor.fetchone()
            return result is not None
        except sqlite3.Error as e:
            # print(f"Error al verificar si la mesa existe en cada partido: {e}")
            return False

    def create_table(self):
        try:
            create_table_query = f"""
                CREATE TABLE IF NOT EXISTS "{self.partido}" (
                    nro_mesa TEXT PRIMARY KEY,
                    {', '.join(f'"{miembro}" INTEGER' for miembro in self.miembros)}
                )
            """
            self.cursor.execute(create_table_query)
            self.conn.commit()
            print("Tabla partido creada con éxito")
        except sqlite3.Error as e:
            print(f"Error al crear la tabla: {e}")

    def update_data(self, values):
        try:
            update_query = f"""
                UPDATE "{self.partido}" SET {', '.join(f'"{miembro}" = ?' for miembro in self.miembros)}
                WHERE nro_mesa = ?;
            """
            self.cursor.execute(update_query, values + [self.nro_mesa])
            self.conn.commit()
            print("Datos actualizados con éxito")
        except sqlite3.Error as e:
            print(f"Error al actualizar los datos: {e}")

    def insert_data(self, values):
        try:
            insert_query = f"""
                INSERT INTO "{self.partido}" (nro_mesa, {', '.join(f'"{miembro}"' for miembro in self.miembros)})
                VALUES (?, {', '.join(['?'] * len(self.miembros))});
            """
            self.cursor.execute(insert_query, [self.nro_mesa] + values)
            self.conn.commit()
            print("Datos insertados con éxito")
        except sqlite3.Error as e:
            print(f"Error al insertar los datos: {e}")

    def recolectarDatos(self):
        try:
            consulta_verificar = f"SELECT name FROM sqlite_master WHERE type='table' AND name='{self.partido}';"
            self.cursor.execute(consulta_verificar)
            tabla_existente = self.cursor.fetchone()

            if tabla_existente:
                todosLosCandidatos = ', '.join(
                    f'`{campo.encode("utf-8").decode("utf-8")}`' for campo in self.miembros)

                consulta = f"SELECT {todosLosCandidatos} FROM {self.partido} WHERE nro_mesa IS NOT NULL"
                self.cursor.execute(consulta)
                registros = self.cursor.fetchall()
                totalVotos = 0

                for tupla in registros:
                    totalVotos += sum(tupla)

                return totalVotos

            else:
                # print(f"La tabla '{self.partido}' no existe.")
                return 0

        except sqlite3.Error as e:
            print("Error al recolectar datos", e)

    def close_connection(self):
        try:
            self.conn.close()
            print("Conexión cerrada")
        except sqlite3.Error as e:
            print(f"Error al cerrar la conexión: {e}")


class MesasDb:
    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()

    def conteo_mesas(self):
        try:
            self.cursor.execute(
                "SELECT nro_mesa FROM mesas ORDER BY nro_mesa ASC")
            list_mesas = [row[0] for row in self.cursor.fetchall()]
            self.conn.close
            return list_mesas
        except sqlite3.Error as e:
            print(f"error en la db : {e}")

    def eliminar_mesa(self):
        def table_exists(cursor, table_name):
            cursor.execute(f"PRAGMA table_info({table_name});")
            return len(cursor.fetchall()) > 0

        try:
            query = "SELECT MAX(nro_mesa) FROM mesas;"
            self.cursor.execute(query)
            ultima_mesa = self.cursor.fetchone()[0]

            if ultima_mesa is not None:
                query = f"DELETE FROM mesas WHERE nro_mesa = {ultima_mesa};"
                self.cursor.execute(query)

                other_tables = [
                    "salvacion_nacional",
                    "centro_democratico",
                    "conservador",
                    "partido_la_u",
                    "Liberal",
                    "Creemos",
                    "nuevo_liberalismo",
                    "cambio_radical",
                    "alianza_verde",
                    "voto_blanco"
                ]

                for table in other_tables:
                    print(table)
                    print(table_exists(self.cursor, table))

                    if table_exists(self.cursor, table):
                        query = f"DELETE FROM {table} WHERE nro_mesa ='Mesa {ultima_mesa}';"
                        print(query)
                        self.cursor.execute(query)

                self.conn.commit()

                print(
                    f"Se eliminó la mesa {ultima_mesa} y los registros relacionados en otras tablas.")
            else:
                print("No hay mesas para eliminar.")

        except sqlite3.Error as e:
            print(
                f"Error al eliminar la última mesa y registros relacionados: {e}")

    def create_mesa(self):
        try:
            create_table_query = """
                CREATE TABLE IF NOT EXISTS mesas (
                    nro_mesa INTEGER PRIMARY KEY AUTOINCREMENT,
                    votosBlanco INTEGER DEFAULT 0
                )
            """
            self.cursor.execute(create_table_query)
            self.conn.commit()
            print("Mesa creada con éxito")
        except sqlite3.Error as e:
            print(f"Error al crear la tabla: {e}")

    def agregar_mesa(self):
        self.cursor.execute("SELECT MAX(nro_mesa) FROM mesas")
        ultima_mesa = self.cursor.fetchone()[0]
        if ultima_mesa is None:
            nuevo_numero_mesa = 1
        else:
            nuevo_numero_mesa = ultima_mesa + 1
        insert_query = "INSERT INTO mesas (nro_mesa) VALUES (?)"
        self.cursor.execute(insert_query, (nuevo_numero_mesa,))
        self.conn.commit()

    def select(self):
        try:
            self.cursor.execute("SELECT COUNT(*) FROM mesas")
            num_mesas = self.cursor.fetchone()[0]
            # print(4, num_mesas)
            if num_mesas == 0:
                self.agregar_mesa()
            return num_mesas

        except sqlite3.Error as e:
            # print(f"Error al verificar si la mesa existe en tabla mesas: {e}")
            return False

    def close_connection(self):
        try:
            self.conn.close()
            print("Conexión cerrada")
        except sqlite3.Error as e:
            print(f"Error al cerrar la conexión: {e}")
