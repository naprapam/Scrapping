#Garis Kemiskinan masing-masing Kabupaten/Kota
GK = {
    6301: 670062,
    6302: 592230,
    6303: 589165,
    6304: 437579,
    6305: 561101,
    6306: 583549,
    6307: 513950,
    6308: 597894,
    6309: 637132,
    6310: 643652,
    6311: 528104,
    6371: 743872,
    6372: 781405
}
df_merge['miskin_moneter'] = df_merge.apply(
    lambda row: 1 if row['KAPITA'] < GK.get(row['R102_new'], np.inf) else 0, axis=1
)

#Garis Kemiskinan Provinsi
GK_prov = {
    6301: 632739,
    6302: 632739,
    6303: 632739,
    6304: 632739,
    6305: 632739,
    6306: 632739,
    6307: 632739,
    6308: 632739,
    6309: 632739,
    6310: 632739,
    6311: 632739,
    6371: 632739,
    6372: 632739
}

df_merge['miskin_moneter_provinsi'] = df_merge.apply(
    lambda row: 1 if row['KAPITA'] < GK_prov.get(row['R102_new'], np.inf) else 0, axis=1
)
