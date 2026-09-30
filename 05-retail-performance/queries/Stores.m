let
    Demo = Binary.Decompress(Binary.FromText("bY47DoNADER7TrEHcMMfahBKiqSIT7CFBUgLloxz/0BAkYOoXLw3nkFloXsLuF14UT/yDB3L5DXCGFqa2H2Zi+HJogPcxn5wiwrRaiTWSKChWcUHePgQIkwtTAH5fY5n1siOgj2cW5T/Pv/FC+sUR8EeLy0qr6ZX1qhO02sL64vpHw==", BinaryEncoding.Base64), Compression.Deflate),
    Source = if DataMode = "Demo" then Demo else if DataMode = "Folder" then File.Contents(DataFolder & "/Stores.csv") else error "DataMode must be Demo or Folder",
    Parsed = Csv.Document(Source, [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.Csv]),
    Headers = Table.PromoteHeaders(Parsed, [PromoteAllScalars=true]),
    Typed = Table.TransformColumnTypes(Headers, {{"StoreID", type text}, {"Store", type text}, {"Region", type text}, {"Format", type text}}, "en-US")
in
    Typed
