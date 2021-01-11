from database.datamanager.dao import DAO
import json


class DataManager(DAO):
    def select_data_list(self, page, per_page):
        sql = "" \
              " SELECT " \
              "     COUNT(id_data) as total " \
              " FROM TBL_DATA "

        row = self.read(sql)
        sql = "" \
              " SELECT " \
              "     FORMAT(@rownum:=@rownum+1, 0) as rownum" \
              "     , id_data" \
              "     , var_path_origin" \
              "     , var_name" \
              "     , date_read(date_create) as date_create" \
              "     , date_read(date_edit) as data_edit" \
              " FROM TBL_DATA, (SELECT @rownum:={0}) TMP " \
              " LIMIT {0}, {1}".format((page - 1) * per_page, per_page)

        return dict({"list": self.read(sql)}, **row[0])

    def select_data_one(self, id_data):
        sql = "" \
              " SELECT " \
              "     TV.id_value" \
              "     , TV.int_num" \
              "     , TV.blob_values" \
              "     , TV.int_decibel" \
              "     , TV.char_is_right" \
              "     , date_read(TV.date_create) as date_create" \
              "     , date_read(TV.date_edit) as data_edit" \
              "     , (SELECT MAX(int_index) FROM TBL_PEAK TP WHERE TP.id_value = TV.id_value) as int_peak" \
              " FROM TBL_VALUE TV " \
              " WHERE id_data = {0}".format(id_data)
        return self.read(sql)

    def select_value_peak(self, id_value):
        sql = "" \
              " SELECT " \
              "     id_peak" \
              "     , int_index" \
              "     , int_decibel" \
              "     , date_read(date_create) as date_create" \
              "     , date_read(date_edit) as data_edit" \
              " FROM TBL_PEAK " \
              " WHERE id_value = %d" \

        return self.read(sql, id_value)

    def insert_data(self, file_path, file_name):
        sql = "" \
              "INSERT INTO TBL_DATA " \
              " (" \
              "     var_path_origin" \
              "     , var_name" \
              " )" \
              "VALUES" \
              " (" \
              "     '{0}'" \
              "     , '{1}'" \
              " )".format(file_path, file_name)
        return self.write(sql)

    def insert_values(self, value_list, file_path):
        res = []
        sql_values = "" \
                     " INSERT INTO TBL_VALUE " \
                     " (" \
                     "     id_data" \
                     "     , int_num" \
                     "     , blob_values" \
                     "     , char_is_right" \
                     " )"

        sql_peak = "" \
                   " INSERT INTO TBL_PEAK " \
                   " (" \
                   "    id_value" \
                   "    , int_index" \
                   " )"

        for j in range(len(value_list)):
            value = value_list[j]

            if j == 0:
                sql_values += " SELECT "
            else:
                sql_values += " UNION SELECT "

            sql_values += "" \
                          "    id_data" \
                          "    , {0}" \
                          "    , '{1}'" \
                          "    , '{2}'" \
                          " FROM TBL_DATA " \
                          " WHERE var_path_origin = '{3}'" \
                          "".format(value["num"], value["value"], "Y" if value["isRight"] else "N", file_path)

            peak_list = value["peak"]

            for k in range(len(peak_list)):
                peak = peak_list[k]

                if j == 0 and k == 0:
                    sql_peak += " SELECT "
                else:
                    sql_peak += " UNION SELECT "

                sql_peak += "" \
                            "   TV.id_value" \
                            "   , {0}" \
                            " FROM TBL_VALUE AS TV LEFT JOIN TBL_DATA AS TD ON TV.id_data = TD.id_data" \
                            " WHERE " \
                            "   TD.var_path_origin = '{1}'" \
                            " AND TV.int_num = {2}" \
                            " AND TV.char_is_right = '{3}'" \
                            "".format(peak, file_path, value["num"], "Y" if value["isRight"] else "N")

        res.append(self.write(sql_values))
        res.append(self.write(sql_peak))

        return res

    def update_peak(self):
        sql = ""
        return self.write(sql)

    def update_value(self):
        sql = ""
        return self.write(sql)

    def delete_data(self):
        sql = ""
        return self.write(sql)

    def delete_data_all(self):
        sql = ""
        return self.write(sql)

    def delete_value(self):
        sql = ""
        return self.write(sql)

    def delete_peak(self):
        sql = ""
        return self.write(sql)
