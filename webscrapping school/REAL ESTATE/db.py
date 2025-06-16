# -*- coding: utf-8 -*-
"""
Created on Fri Oct  1 12:32:10 2021

@author: Asad Mehmood (asadmahmood16@hotmail.com)
"""

import mysql.connector
import logging


def reconnect(instance):
    try:
        if not instance.connection.is_connected():
            instance.print_log("Connection lost. Reconnecting...", True)
            instance.connection.reconnect(attempts=3, delay=5)
            instance.cursor = instance.connection.cursor()
            instance.print_log("Reconnected to MySQL server.")
        else:
            instance.print_log("Connection is already active.")
    except Exception as e:
        instance.print_log(f"Reconnection failed: {e}", True)
        raise


class Mysql:
	def __init__(self, dev=True):
		self.dev = dev
		db_base = "cashprohomebuyer_new_real_state"
		config = {
			'user': "cashprohomebuyer_new_real_state",
			'password': "KH8lhGoLK4Sl",
			'host': "104.238.220.190",
			'database': db_base
		}

		self.connection = mysql.connector.connect(**config)
		if self.connection.is_connected():
			self.cursor = self.connection.cursor()
			self.print_log("Database Connected: '{}'".format(db_base))
		else:
			self.print_log("Unable to Connect: '{}'".format(db_base))

	def print_log(self, text, error=False):
		dev = self.dev
		if dev:
			print(text)
		else:
			if error:
				logging.error(text.strip())
			else:
				logging.info(text.strip())

	def njpub(self, data):
		reconnect(self)
		table_name = "NjPub"
		data = {
			**data,
			'table_name': table_name
		}

		key_list = list(data.keys())
		val_list = list()
		for value in data.values():
			if type(value) == str:
				value = value.replace('\'', '')
				values = f"'{value}'"
				val_list.append(values)
			else:
				if not bool(value):
					values = "-1"
					val_list.append(values)
				else:
					values = f"{value}"
					val_list.append(values)

		street, city = data['Street'], data['City']
		query = None
		address = False
		if bool(street) and bool(city):
			query = "SELECT COUNT(1) FROM `{table_name}` WHERE `Street` = '{Street}' AND `City` = '{City}';".format_map(
				data)
			address = True
		else:
			query = "SELECT COUNT(1) FROM `{table_name}` WHERE `Notice` = '{Notice}';".format_map(data)
		self.cursor.execute(query)
		rows = self.cursor.fetchall()
		if bool(rows[0][0]):
			set_equal = list()
			skip_columns = ['table_name']
			if bool(address):
				skip_columns.extend(['Street', 'City'])
			else:
				skip_columns.append('Notice')
			for column, values in zip(key_list, val_list):
				if column in skip_columns:
					continue
				sets = "{} = {}".format(column, values)
				set_equal.append(sets)
			equals = ", ".join(set_equal)

			where_clause = None
			if address:
				where_clause = "`Street` = '{Street}' AND `City` = '{City}'".format_map(data)
			else:
				where_clause = "`Notice` = '{Notice}'".format_map(data)

			stmt = """UPDATE `{}` SET {} WHERE {};""".format(table_name, equals, where_clause)
		else:
			key_list.remove('table_name')
			val_list.remove("'{}'".format(table_name))
			columns_str = "`, `".join(key_list)
			values = ", ".join(val_list)

			stmt = "INSERT INTO `{}` (`{}`) VALUES ({});".format(table_name, columns_str, values)

		try:
			self.run_query(stmt)
			if stmt.startswith("UPDATE"):
				self.print_log("\nData Updated: '{}'".format(data['Id']))
			else:
				self.print_log("\nData Inserted: '{}'".format(data['Id']))
		except Exception as e:
			error_str = "{}: {}".format(str(type(e).__name__), str(e))
			error_sql = "SQL: '{}'".format(stmt)
			self.print_log(error_str, True)
			self.print_log(error_sql, True)

	def ctpub(self, data):
		reconnect(self)
		table_name = "CtPub"
		data = {
			**data,
			'table_name': table_name
		}

		key_list = list(data.keys())
		val_list = list()
		for value in data.values():
			if type(value) == str:
				value = value.replace('\'', '')
				values = f"'{value}'"
				val_list.append(values)
			else:
				if not bool(value):
					values = "-1"
					val_list.append(values)
				else:
					values = f"{value}"
					val_list.append(values)

		street, city = data['Street'], data['City']
		query = None
		address = False
		if bool(street) and bool(city):
			query = "SELECT COUNT(1) FROM `{table_name}` WHERE `Street` = '{Street}' AND `City` = '{City}';".format_map(
				data)
			address = True
		else:
			query = "SELECT COUNT(1) FROM `{table_name}` WHERE `Notice` = '{Notice}';".format_map(data)

		self.cursor.execute(query)
		rows = self.cursor.fetchall()
		if bool(rows[0][0]):
			set_equal = list()
			skip_columns = ['table_name']
			if bool(address):
				skip_columns.extend(['Street', 'City'])
			else:
				skip_columns.append('Notice')
			for column, values in zip(key_list, val_list):
				if column in skip_columns:
					continue
				sets = "{} = {}".format(column, values)
				set_equal.append(sets)
			equals = ", ".join(set_equal)

			where_clause = None
			if address:
				where_clause = "`Street` = '{Street}' AND `City` = '{City}'".format_map(data)
			else:
				where_clause = "`Notice` = '{Notice}'".format_map(data)

			stmt = """UPDATE `{}` SET {} WHERE {};""".format(table_name, equals, where_clause)
		else:
			key_list.remove('table_name')
			val_list.remove("'{}'".format(table_name))
			columns_str = "`, `".join(key_list)
			values = ", ".join(val_list)

			stmt = "INSERT INTO `{}` (`{}`) VALUES ({});".format(table_name, columns_str, values)

		try:
			self.run_query(stmt)
			if stmt.startswith("UPDATE"):
				self.print_log("\nData Updated: '{}'".format(data['Id']))
			else:
				self.print_log("\nData Inserted: '{}'".format(data['Id']))
		except Exception as e:
			error_str = "{}: {}".format(str(type(e).__name__), str(e))
			error_sql = "SQL: '{}'".format(stmt)
			self.print_log(error_str, True)
			self.print_log(error_sql, True)

	def papub(self, data):
		reconnect(self)
		table_name = "PaPub"
		data = {
			**data,
			'table_name': table_name
		}
		key_list = list(data.keys())
		val_list = list()
		for value in data.values():
			if type(value) == str:
				value = value.replace('\'', '')
				values = f"'{value}'"
				val_list.append(values)
			else:
				if not bool(value):
					values = "-1"
					val_list.append(values)
				else:
					values = f"{value}"
					val_list.append(values)

		street, city = data['Street'], data['City']
		query = None
		address = False
		if bool(street) and bool(city):
			query = "SELECT COUNT(1) FROM `{table_name}` WHERE `Street` = '{Street}' AND `City` = '{City}';".format_map(
				data)
			address = True
		else:
			query = "SELECT COUNT(1) FROM `{table_name}` WHERE `Notice` = '{Notice}';".format_map(data)
		self.cursor.execute(query)
		rows = self.cursor.fetchall()
		if bool(rows[0][0]):
			set_equal = list()
			skip_columns = ['table_name']
			if bool(address):
				skip_columns.extend(['Street', 'City'])
			else:
				skip_columns.append('Notice')
			for column, values in zip(key_list, val_list):
				if column in skip_columns:
					continue
				sets = "{} = {}".format(column, values)
				set_equal.append(sets)
			equals = ", ".join(set_equal)

			where_clause = None
			if address:
				where_clause = "`Street` = '{Street}' AND `City` = '{City}'".format_map(data)
			else:
				where_clause = "`Notice` = '{Notice}'".format_map(data)

			stmt = """UPDATE `{}` SET {} WHERE {};""".format(table_name, equals, where_clause)
		else:
			key_list.remove('table_name')
			val_list.remove("'{}'".format(table_name))
			columns_str = "`, `".join(key_list)
			values = ", ".join(val_list)

			stmt = "INSERT INTO `{}` (`{}`) VALUES ({});".format(table_name, columns_str, values)

		try:
			self.run_query(stmt)
			if stmt.startswith("UPDATE"):
				self.print_log("\nData Updated: '{}'".format(data['Id']))
			else:
				self.print_log("\nData Inserted: '{}'".format(data['Id']))
		except Exception as e:
			error_str = "{}: {}".format(str(type(e).__name__), str(e))
			error_sql = "SQL: '{}'".format(stmt)
			self.print_log(error_str, True)
			self.print_log(error_sql, True)

	def nypub(self, data):
		reconnect(self)
		table_name = "NyPub"
		data = {
			**data,
			'table_name': table_name
		}

		key_list = list(data.keys())
		val_list = list()
		for value in data.values():
			if type(value) == str:
				value = value.replace('\'', '')
				values = f"'{value}'"
				val_list.append(values)
			else:
				if not bool(value):
					values = "-1"
					val_list.append(values)
				else:
					values = f"{value}"
					val_list.append(values)

		street, city = data['Street'], data['City']
		query = None
		address = False
		if bool(street) and bool(city):
			query = "SELECT COUNT(1) FROM `{table_name}` WHERE `Street` = '{Street}' AND `City` = '{City}';".format_map(
				data)
			address = True
		else:
			query = "SELECT COUNT(1) FROM `{table_name}` WHERE `Notice` = '{Notice}';".format_map(data)

		self.cursor.execute(query)
		rows = self.cursor.fetchall()
		if bool(rows[0][0]):
			set_equal = list()
			skip_columns = ['table_name']
			if bool(address):
				skip_columns.extend(['Street', 'City'])
			else:
				skip_columns.append('Notice')
			for column, values in zip(key_list, val_list):
				if column in skip_columns:
					continue
				sets = "{} = {}".format(column, values)
				set_equal.append(sets)
			equals = ", ".join(set_equal)

			where_clause = None
			if address:
				where_clause = "`Street` = '{Street}' AND `City` = '{City}'".format_map(data)
			else:
				where_clause = "`Notice` = '{Notice}'".format_map(data)

			stmt = """UPDATE `{}` SET {} WHERE {};""".format(table_name, equals, where_clause)
		else:
			key_list.remove('table_name')
			val_list.remove("'{}'".format(table_name))
			columns_str = "`, `".join(key_list)
			values = ", ".join(val_list)

			stmt = "INSERT INTO `{}` (`{}`) VALUES ({});".format(table_name, columns_str, values)

		try:
			self.run_query(stmt)
			if stmt.startswith("UPDATE"):
				self.print_log("\nData Updated: '{}'".format(data['Id']))
			else:
				self.print_log("\nData Inserted: '{}'".format(data['Id']))
		except Exception as e:
			error_str = "{}: {}".format(str(type(e).__name__), str(e))
			error_sql = "SQL: '{}'".format(stmt)
			self.print_log(error_str, True)
			self.print_log(error_sql, True)

	def gapub(self, data):
		reconnect(self)
		table_name = "GaPub"
		data = {
			**data,
			'table_name': table_name
		}
		key_list = list(data.keys())
		val_list = list()
		for value in data.values():
			if type(value) == str:
				value = value.replace('\'', '')
				values = f"'{value}'"
				val_list.append(values)
			else:
				if not bool(value):
					values = "-1"
					val_list.append(values)
				else:
					values = f"{value}"
					val_list.append(values)

		street, city = data['Street'], data['City']
		query = None
		address = False
		if bool(street) and bool(city):
			query = "SELECT COUNT(1) FROM `{table_name}` WHERE `Street` = '{Street}' AND `City` = '{City}';".format_map(
				data)
			address = True
		else:
			query = "SELECT COUNT(1) FROM `{table_name}` WHERE `Notice` = '{Notice}';".format_map(data)
		self.cursor.execute(query)
		rows = self.cursor.fetchall()
		if bool(rows[0][0]):
			set_equal = list()
			skip_columns = ['table_name']
			if bool(address):
				skip_columns.extend(['Street', 'City'])
			else:
				skip_columns.append('Notice')
			for column, values in zip(key_list, val_list):
				if column in skip_columns:
					continue
				sets = "{} = {}".format(column, values)
				set_equal.append(sets)
			equals = ", ".join(set_equal)

			where_clause = None
			if address:
				where_clause = "`Street` = '{Street}' AND `City` = '{City}'".format_map(data)
			else:
				where_clause = "`Notice` = '{Notice}'".format_map(data)

			stmt = """UPDATE `{}` SET {} WHERE {};""".format(table_name, equals, where_clause)
		else:
			key_list.remove('table_name')
			val_list.remove("'{}'".format(table_name))
			columns_str = "`, `".join(key_list)
			values = ", ".join(val_list)

			stmt = "INSERT INTO `{}` (`{}`) VALUES ({});".format(table_name, columns_str, values)

		try:
			self.run_query(stmt)
			if stmt.startswith("UPDATE"):
				self.print_log("\nData Updated: '{}'".format(data['Id']))
			else:
				self.print_log("\nData Inserted: '{}'".format(data['Id']))
		except Exception as e:
			error_str = "{}: {}".format(str(type(e).__name__), str(e))
			error_sql = "SQL: '{}'".format(stmt)
			self.print_log(error_str, True)
			self.print_log(error_sql, True)

		print("+++DB FUNCTION COMPLETED+++")


	def v3mls(self, data):
		reconnect(self)
		self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS V3Mls (
                Table_Index INT,
                Street VARCHAR(100) PRIMARY KEY,
                City VARCHAR(100),
                State CHAR(2),
                Zip_Code VARCHAR(10),
                Bedrooms VARCHAR(10),
                Bathrooms VARCHAR(10),
                Listing_Type VARCHAR(10),
                Class VARCHAR(10)
            );''')

		data = {
			**data,
			'Table_Index': self.get_count('V3Mls')
		}

		keys = [
			'Table_Index',
			'Street',
			'City',
			'State',
			'Zip Code',
			'Bedrooms',
			'Bathrooms',
			'Listing Type',
			'Class'
		]

		values = ''

		for key in keys:
			value = data[key]
			if type(value) == str:
				value = value.replace('\'', '')
				values += f"'{value}', "
			else:
				if not value:
					values += " '', "
				else:
					values += f"{value}, "

		values = values.rstrip(', ')
		stmt = f"INSERT INTO V3Mls VALUES ({values});"
		try:
			self.cursor.execute(stmt)
		except Exception as e:
			error_str = "{}: {}".format(str(type(e).__name__), str(e))
			error_sql = "SQL: '{}'".format(stmt)
			self.print_log(error_str, True)
			self.print_log(error_sql, True)

	def nymls(self, data):
		reconnect(self)
		table_name = "NyStateMLS"

		keys = list()
		val_list = list()
		for key, value in data.items():
			if type(value) == str:
				value = value.replace('\'', '')
			val_list.append(f"'{value}'")
			keys.append(key)

		listing_id = data['Listing ID']
		address = data['Address']

		if 'Lot Sq. Ft.' in data.keys():
			data['Lot_Sq_Ft'] = data['Lot Sq. Ft.']
			del data['Lot Sq. Ft.']

		key_list = [k.replace(" ", "_") for k in data.keys()]

		has_address = False
		ind_val = False
		if not ind_val:
			query = "SELECT COUNT(1) FROM `{}` WHERE `Address` = '{}';".format(table_name, address)
			self.cursor.execute(query)
			rows = self.cursor.fetchall()
			add_val = rows[0][0]
			if bool(add_val):
				has_address = True

		if bool(ind_val) or bool(add_val):
			set_equal = list()

			skip_column = 'Listing_ID'
			if has_address:
				skip_column = 'Address'

			for column, values in zip(key_list, val_list):
				if column == skip_column:
					continue
				sets = "`{}` = {}".format(column, values)
				set_equal.append(sets)
			equals = ", ".join(set_equal)

			where_clause = None
			if has_address:
				where_clause = "`Address` = '{}'".format(address)
			else:
				where_clause = "`Listing_ID` = '{}'".format(listing_id)

			stmt = """UPDATE `{}` SET {} WHERE {};""".format(table_name, equals, where_clause)
		else:
			columns_str = "`, `".join(key_list)
			values = ", ".join(val_list)

			stmt = "INSERT INTO `{}` (`{}`) VALUES ({});".format(table_name, columns_str, values)

		try:
			self.cursor.execute(stmt)
			self.cursor.execute("COMMIT;")
			if stmt.startswith("UPDATE"):
				self.print_log("\nData Updated: '{}'".format(listing_id))
			else:
				self.print_log("\nData Inserted: '{}'".format(listing_id))
		except Exception as e:
			error_str = "{}: {}".format(str(type(e).__name__), str(e))
			error_sql = "SQL: '{}'".format(stmt)
			self.print_log(error_str, True)
			self.print_log(error_sql, True)

	def zillow(self, data):
		reconnect(self)
		table_name = "Zillow"
		count_row = self.get_count(table_name, 'Table_Index') + 1
		data = {
			**data,
			'Table_Index': count_row
		}

		values = None
		key_list = list()
		val_list = list()
		for key, value in data.items():
			if type(value) == str:
				value = value.replace('\'', '')
				values = f"'{value}'"
				val_list.append(values)
				key_list.append(key)
			else:
				if not bool(value):
					values = "-1"
					val_list.append(values)
					key_list.append(key)
				else:
					values = f"{value}"
					val_list.append(values)
					key_list.append(key)

		values = ", ".join(val_list)
		columns_str = "`, `".join(key_list)
		ID = data['Id']

		run_stmt = False
		query = "SELECT `{}` FROM `{}` WHERE `Id` = {};".format(columns_str, table_name, ID)
		self.cursor.execute(query)
		rows = self.cursor.fetchone()
		if bool(rows):
			all_values = list(data.values())

			set_equal = list()
			skip_columns = ['Id', 'Table_Index']
			for column, values, new_val in zip(key_list, val_list, all_values):
				if column in skip_columns:
					continue
				sets = "{} = {}".format(column, values)
				set_equal.append(sets)

			if bool(set_equal):
				equals = ", ".join(set_equal)
				stmt = """UPDATE `{}` SET {} WHERE `Id` = {};""".format(table_name, equals, ID)
				run_stmt = True
		else:
			stmt = "INSERT INTO `{}` (`{}`) VALUES ({});".format(table_name, columns_str, values)
			run_stmt = True

		if run_stmt:
			try:
				self.run_query(stmt)
				if stmt.startswith("UPDATE"):
					self.print_log("\nData Updated: '{}'".format(data['Id']))
				else:
					self.print_log("\nData Inserted: '{}'".format(data['Id']))
			except Exception as e:
				error_str = "{}: {}".format(str(type(e).__name__), str(e))
				error_sql = "SQL: '{}'".format(stmt)
				self.print_log(error_str, True)
				self.print_log(error_sql, True)

	def ussearch(self, data, dest_data):
		reconnect(self)
		table_name = "UsSearch"
		values = None
		key_list = list()
		val_list = list()
		for key, value in data.items():
			if type(value) == str:
				value = value.replace('\'', '')
				values = f"'{value}'"
				val_list.append(values)
				key_list.append(key)
			else:
				if not bool(value):
					values = "-1"
					val_list.append(values)
					key_list.append(key)
				else:
					values = f"{value}"
					val_list.append(values)
					key_list.append(key)

		values = ", ".join(val_list)
		columns_str = "`, `".join(key_list)
		name = data['Name']

		update = False
		query = "SELECT Table_Index FROM `{}` WHERE `Name` = '{}';".format(table_name, name)
		self.cursor.execute(query)
		rows = self.cursor.fetchall()
		if bool(rows) and bool(rows[0][0]):
			row_id = rows[0][0]
			set_equal = list()
			skip_columns = ['Name', 'offer_price']
			for column, values in zip(key_list, val_list):
				if column in skip_columns:
					continue
				sets = "{} = {}".format(column, values)
				set_equal.append(sets)
			equals = ", ".join(set_equal)
			stmt = """UPDATE {} SET {} WHERE `Name` = '{}';""".format(table_name, equals, name)
			update = True
		else:
			stmt = "INSERT INTO `{}` (`{}`) VALUES ({});".format(table_name, columns_str, values)

		try:
			if update:
				self.run_query(stmt)
			else:
				self.cursor.execute(stmt)
				row_id = self.cursor.lastrowid
				self.cursor.execute("COMMIT;")

			if stmt.startswith("UPDATE"):
				self.print_log("\nData Updated: '{}'".format(row_id))
			else:
				self.print_log("\nData Inserted: '{}'".format(row_id))
		except Exception as e:
			error_str = "{}: {}".format(str(type(e).__name__), str(e))
			error_sql = "SQL: '{}'".format(stmt)
			self.print_log(error_str, True)
			self.print_log(error_sql, True)

		if dest_data:
			dest_data.update({'UsSearch_ID': row_id})
			up_stmt = "UPDATE `{table_name}` SET `UsSearch_ID` = {UsSearch_ID} WHERE `Table_Index` = {Table_Index};".format_map(
				dest_data)
			table_dest = dest_data['table_name']
			if table_dest == "NyStateMLS":
				up_stmt = "UPDATE `{table_name}` SET `UsSearch_ID` = {UsSearch_ID} WHERE `Listing_Id` = '{Table_Index}';".format_map(
					dest_data)
			try:
				self.run_query(up_stmt)
				self.print_log("Updated Table `{table_name}` at Index = {Table_Index}".format_map(dest_data))
			except Exception as e:
				error_str = "{}: {}".format(str(type(e).__name__), str(e))
				error_sql = "SQL: '{}'".format(up_stmt)
				self.print_log(error_str, True)
				self.print_log(error_sql, True)

	def batchfind(self, data, dest_data):
		reconnect(self)
		table_name = "Batchfind"
		values = None
		key_list = list()
		val_list = list()
		for key, value in data.items():
			if type(value) == str:
				value = value.replace('\'', '')
				values = f"'{value}'"
				val_list.append(values)
				key_list.append(key)
			else:
				if not bool(value):
					values = "-1"
					val_list.append(values)
					key_list.append(key)
				else:
					values = f"{value}"
					val_list.append(values)
					key_list.append(key)

		values = ", ".join(val_list)
		columns_str = "`, `".join(key_list)
		listing_id = data['listing_id']

		update = False
		query = "SELECT Table_Index FROM `{}` WHERE `listing_id` = '{}';".format(table_name, listing_id)
		self.cursor.execute(query)
		rows = self.cursor.fetchall()
		if bool(rows) and bool(rows[0][0]):
			row_id = rows[0][0]
			set_equal = list()
			skip_columns = ['Name', 'offer_price']
			for column, values in zip(key_list, val_list):
				if column in skip_columns:
					continue
				sets = "{} = {}".format(column, values)
				set_equal.append(sets)
			equals = ", ".join(set_equal)
			stmt = """UPDATE {} SET {} WHERE `listing_id` = '{}';""".format(table_name, equals, listing_id)
			update = True
		else:
			stmt = "INSERT INTO `{}` (`{}`) VALUES ({});".format(table_name, columns_str, values)

		try:
			if update:
				self.run_query(stmt)
			else:
				self.cursor.execute(stmt)
				row_id = self.cursor.lastrowid
				self.cursor.execute("COMMIT;")

			if stmt.startswith("UPDATE"):
				self.print_log("\nData Updated: '{}'".format(row_id))
			else:
				self.print_log("\nData Inserted: '{}'".format(row_id))
		except Exception as e:
			error_str = "{}: {}".format(str(type(e).__name__), str(e))
			error_sql = "SQL: '{}'".format(stmt)
			self.print_log(error_str, True)
			self.print_log(error_sql, True)

		if dest_data:
			dest_data.update({'Batchfind': row_id})
			up_stmt = "UPDATE `{table_name}` SET `Batchfind` = {Batchfind} WHERE `Table_Index` = {Table_Index};".format_map(
				dest_data)

			try:
				self.run_query(up_stmt)
				self.print_log("Updated Table `{table_name}` at Index = {Table_Index}".format_map(dest_data))
			except Exception as e:
				error_str = "{}: {}".format(str(type(e).__name__), str(e))
				error_sql = "SQL: '{}'".format(up_stmt)
				self.print_log(error_str, True)
				self.print_log(error_sql, True)

	def batchleads_log(self, data):
		reconnect(self)
		table_name = "Batchleads_log"
		values = None
		key_list = list()
		val_list = list()
		for key, value in data.items():
			if type(value) == str:
				value = value.replace('\'', '')
				values = f"'{value}'"
				val_list.append(values)
				key_list.append(key)
			else:
				if not bool(value):
					values = "-1"
					val_list.append(values)
					key_list.append(key)
				else:
					values = f"{value}"
					val_list.append(values)
					key_list.append(key)

		values = ", ".join(val_list)
		columns_str = "`, `".join(key_list)
		source = data['Data_Source']

		query = "SELECT COUNT(1) FROM `{}` WHERE `Data_Source` = '{}';".format(table_name, source)
		self.cursor.execute(query)
		rows = self.cursor.fetchall()
		if bool(rows) and bool(rows[0][0]):
			set_equal = list()
			skip_columns = ['Name', 'offer_price']
			for column, values in zip(key_list, val_list):
				if column in skip_columns:
					continue
				sets = "{} = {}".format(column, values)
				set_equal.append(sets)
			equals = ", ".join(set_equal)
			stmt = """UPDATE {} SET {} WHERE `Data_Source` = '{}';""".format(table_name, equals, source)
		else:
			stmt = "INSERT INTO `{}` (`{}`) VALUES ({});".format(table_name, columns_str, values)

		try:
			self.cursor.execute(stmt)
			self.cursor.execute("COMMIT;")
			if stmt.startswith("UPDATE"):
				self.print_log("\nData Updated: '{}'".format(source))
			else:
				self.print_log("\nData Inserted: '{}'".format(source))
		except Exception as e:
			error_str = "{}: {}".format(str(type(e).__name__), str(e))
			error_sql = "SQL: '{}'".format(stmt)
			self.print_log(error_str, True)
			self.print_log(error_sql, True)

	def zestimate(self, data, dest_data=False):
		reconnect(self)
		table_name = "Zestimate"
		values = None
		key_list = list()
		val_list = list()
		for key, value in data.items():
			if key == "Status":
				continue
			if type(value) == str:
				value = value.replace('\'', '')
				values = f"'{value}'"
				val_list.append(values)
				key_list.append(key)
			else:
				if not bool(value):
					values = "-1"
					val_list.append(values)
					key_list.append(key)
				else:
					values = f"{value}"
					val_list.append(values)
					key_list.append(key)

		values = ", ".join(val_list)
		columns_str = "`, `".join(key_list)
		ID = data['Id']

		query = "SELECT COUNT(1) FROM `{}` WHERE `Id` = {};".format(table_name, ID)
		self.cursor.execute(query)
		rows = self.cursor.fetchall()
		if bool(rows[0][0]):
			set_equal = list()
			for column, values in zip(key_list, val_list):
				if column == 'Id':
					continue
				sets = "`{}` = {}".format(column, values)
				set_equal.append(sets)
			equals = ", ".join(set_equal)
			stmt = """UPDATE {} SET {} WHERE `Id` = {};""".format(table_name, equals, ID)
		else:
			stmt = "INSERT INTO `{}` (`{}`) VALUES ({});".format(table_name, columns_str, values)

		try:
			self.run_query(stmt)
			if stmt.startswith("UPDATE"):
				self.print_log("\nData Updated: '{}'".format(ID))
			else:
				self.print_log("\nData Inserted: '{}'".format(ID))
		except Exception as e:
			error_str = "{}: {}".format(str(type(e).__name__), str(e))
			error_sql = "SQL: '{}'".format(stmt)
			self.print_log(error_str, True)
			self.print_log(error_sql, True)

		if dest_data:
			update_parent = True
			dest_table = dest_data['table_name']
			dest_Index = dest_data['Table_Index']
			z_pid = dest_data['zpid']

			where_clause = "`Table_Index` = {}".format(dest_Index)
			stmt_upd = "UPDATE `{}` SET `zpid` = {} WHERE {};".format(dest_table, z_pid, where_clause)

			stmt_sel = "SELECT `zpid` FROM {} WHERE {};".format(dest_table, where_clause)
			self.cursor.execute(stmt_sel)
			row_zpid = self.cursor.fetchone()
			exist_zpid = row_zpid[0]
			if bool(exist_zpid):
				update_parent = False

			if update_parent:
				try:
					self.run_query(stmt_upd)
					self.print_log("Updated Table `{table_name}` at Index = {Table_Index}".format_map(dest_data))
				except Exception as e:
					error_str = "{}: {}".format(str(type(e).__name__), str(e))
					error_sql = "SQL: '{}'".format(stmt_upd)
					self.print_log(error_str, True)
					self.print_log(error_sql, True)

	def show_data(self, name, extra=False):
		reconnect(self)
		stmt = 'SELECT * FROM {};'.format(name)
		if extra:
			if isinstance(extra, list):
				columns = extra.copy()
				column_str = ", ".join(columns)
				stmt = 'SELECT {} FROM {};'.format(column_str, name)
			elif isinstance(extra, str):
				stmt = extra.strip()

		self.cursor.execute(stmt)
		rows = self.cursor.fetchall()
		for row in rows:
			yield row
			# print("++++++++",row)

	def get_count(self, name, max_column=False):
		reconnect(self)
		stmt = 'SELECT COUNT(1) FROM {};'.format(name)
		if max_column:
			stmt = 'SELECT MAX({}) FROM {};'.format(max_column, name)
		self.cursor.execute(stmt)
		rows = self.cursor.fetchall()
		return rows[0][0]

	def run_query(self, query):
		self.cursor.execute(query)
		self.cursor.execute("COMMIT")

	def Close_db(self):
		if self.connection.is_connected():
			self.cursor.close()
			self.connection.close()
			self.print_log("Database Connection Close.")

	def ecourts(self, data):
		table_name = "ECourts"
		data = {
			**data,
			'table_name': table_name
		}

		key_list = list(data.keys())
		val_list = list()
		for value in data.values():
			if type(value) == str:
				value = value.replace('\'', '')
				values = f"'{value}'"
				val_list.append(values)
			else:
				if not bool(value):
					values = "-1"
					val_list.append(values)
				else:
					values = f"{value}"
					val_list.append(values)

		# street, city = data['Street'], data['City']
		query = "SELECT COUNT(1) FROM `{table_name}` WHERE `INDEX_NUMBER` = '{INDEX_NUMBER}';".format_map(data)

		self.cursor.execute(query)
		rows = self.cursor.fetchall()
		if bool(rows[0][0]):
			set_equal = list()
			skip_columns = ['table_name']
			for column, values in zip(key_list, val_list):
				if column in skip_columns:
					continue
				sets = "{} = {}".format(column, values)
				set_equal.append(sets)
			equals = ", ".join(set_equal)

			where_clause = "`INDEX_NUMBER` = '{INDEX_NUMBER}'".format_map(data)

			stmt = """UPDATE `{}` SET {} WHERE {};""".format(table_name, equals, where_clause)
		else:
			key_list.remove('table_name')
			val_list.remove("'{}'".format(table_name))
			columns_str = "`, `".join(key_list)
			values = ", ".join(val_list)

			stmt = "INSERT INTO `{}` (`{}`) VALUES ({});".format(table_name, columns_str, values)

		try:
			self.run_query(stmt)
			u_id = data['INDEX_NUMBER']
			if stmt.startswith("UPDATE"):
				self.print_log("\nData Updated: '{}'".format(u_id))
			else:
				self.print_log("\nData Inserted: '{}'".format(u_id))
		except Exception as e:
			error_str = "{}: {}".format(str(type(e).__name__), str(e))
			error_sql = "SQL: '{}'".format(stmt)
			self.print_log(error_str, True)
			self.print_log(error_sql, True)


def db_remove_dups():
	reconnect(self)
	db = Mysql()
	table_name = "CtPub"
	column_names = ['Street', 'City', 'State', 'Zip_Code', 'Publisher', 'Id', 'Notice', 'Address', 'Date_Added',
	                'Reiskip_ID', 'UsSearch_ID', 'Infofree_ID', 'Oasis_ID', 'Facebook_ID', 'Linkedin_ID', 'zpid',
	                'Batchfind']
	rows = db.show_data(table_name, column_names)

	for row in rows:
		values = dict()
		for col, val in zip(column_names, row):
			if not bool(val):
				val = ''

			if col == "Notice" and bool(val):
				val = val.strip().replace('\'', '')

			if col == "Street" and bool(val) and val.startswith(":"):
				val = val.replace(":", "").strip()

			if col in ['Street', 'City'] and not bool(val):
				values[col] = val.strip()

			if bool(val):
				values[col] = val
				if isinstance(val, str):
					values[col] = val.strip()

		db.ctpub(values)
	db.Close_db()


if __name__ == "__main__":
	pass