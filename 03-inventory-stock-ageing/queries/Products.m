let
    Demo = Binary.Decompress(Binary.FromText("fZM9bgJBDIV7TsEBpmBs81dG0ERpkEgOQMgqQgIG7UKR22ckWxF5Hm83ll7heZ+/XV++Hsf76zbt9JU2h3v3XfqftH/cbudT10/2bx+zWU7b7lKmlprW+b2U8/CXmpLmCHKUXo7HbhhKf+qe0qxphjSnTbkOj8vh8/ycFk0LpCXtDv39KTfX3Bxyc9x1obkF5BbtXbOml5Betne1HlaQXuGu1sAacmvcVf+eZ/9zdW7uqg1koFXn5q7aQwZmdYZdtYEMtOrcvIEMnOo8cgMZaNV55AYyMKtz8wYy0Kpz8wYycKrzyA1koFXnkRsgYFbn5g0Q0CLnlv6dgBMFbmkDBLQocEt7IGBGzi1tgIAWObfs78CJAresAaBFgVvWAzAj55Y1ALTIuaV/Z+DEgVvaAAMtDtzSHhiYsXNLG2Cgxc4t/TsDJw7c0gYYaHHglvUAzNi5ZQ0ALXZu2d+BEwduWQNAiwO3tAcBZuLc0gYEaIlzS/8uwEkCt7QBAVoSuKU9CDAT55Y2IEBLnFv2d+AkgVvWANCSwC3rAZiJcytPfgE=", BinaryEncoding.Base64), Compression.Deflate),
    Source = if DataMode = "Demo" then Demo else if DataMode = "Folder" then File.Contents(DataFolder & "/Products.csv") else error "DataMode must be Demo or Folder",
    Parsed = Csv.Document(Source, [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.Csv]),
    Headers = Table.PromoteHeaders(Parsed, [PromoteAllScalars=true]),
    Typed = Table.TransformColumnTypes(Headers, {{"ProductID", type text}, {"Product", type text}, {"Category", type text}, {"Supplier", type text}}, "en-US")
in
    Typed
