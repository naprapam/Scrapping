# Database dengan ekstensi .dbf
from dbfread import DBF, FieldParser
import pandas as pd

# Custom parser yang membiarkan "." jadi None (NaN nanti di Pandas)
class CustomFieldParser(FieldParser):
    def parseN(self, field, data):
        data = data.strip()
        if data in (b'.', b'', b' '):
            return None
        try:
            return int(data)
        except ValueError:
            try:
                return float(data.replace(b',', b'.'))
            except ValueError:
                return None
# Baca DBF dengan parser custom
table1 = DBF('63_ssn_202403_kor_ind1.dbf', encoding='latin1',
            parserclass=CustomFieldParser, ignore_missing_memofile=True)
table2 = DBF('63_ssn_202403_kor_ind2.dbf', encoding='latin1',
            parserclass=CustomFieldParser, ignore_missing_memofile=True)
table3 = DBF('63_ssn_202403_kor_rt.dbf', encoding='latin1',
            parserclass=CustomFieldParser, ignore_missing_memofile=True)
table4 = DBF('63_ssn_202403_kp_blok43.dbf', encoding='latin1',
            parserclass=CustomFieldParser, ignore_missing_memofile=True)

# Konversi ke DataFrame Pandas
df1 = pd.DataFrame(iter(table1))
df2 = pd.DataFrame(iter(table2))
df3 = pd.DataFrame(iter(table3))
df4 = pd.DataFrame(iter(table4))

#Merger dengan one-on-one
df_concat1 = pd.concat([df1, df2], axis=1)
df_concat2 = pd.concat([df3, df4], axis=1)

#Merger dengan one-to-many
df_merge = pd.merge(df_concat1, df_concat2, how='inner')
df_merge
