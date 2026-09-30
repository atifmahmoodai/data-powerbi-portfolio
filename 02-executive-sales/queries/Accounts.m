let
    Demo = Binary.Decompress(Binary.FromText("hZJNboMwFIT3PQUHcCX8gPwsadJFF+minAAlVooacGRMz98xUrOYGLP95IF5+qY+n+00+I+jOkyjt71x6stcOzuoxlx7M3jVtDcz3o0b7fBS57lWR9Pb7P91BvBpnf9Wp+7y2rfux3hVX3670bpMQkA4IOqA77r2pt4Hb9zddaN5RIoQKThSqMZO+Edzenu8LMPLkl+Wy22qEKg4UKXa6BDZcGQTaTOfuuWX2+U286E7DuxSbeaL9xzZR9qEU3VOLwEW24RDNasFSLQJF2uWC/DcJpyq2SnAYptwqGa1AIk288UsF+C5zXwqOwVIrlizWoCVFWuWCxBfsWanAMkVC6sFWFmxsFyA+IqFnQIkVyysFmBlxcJyAeIrFnYKkFyxsFqAlRULywWIr1jYKUByxcJqAVZWXLBcgNiK/wA=", BinaryEncoding.Base64), Compression.Deflate),
    Source = if DataMode = "Demo" then Demo else if DataMode = "Folder" then File.Contents(DataFolder & "/Accounts.csv") else error "DataMode must be Demo or Folder",
    Parsed = Csv.Document(Source, [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.Csv]),
    Headers = Table.PromoteHeaders(Parsed, [PromoteAllScalars=true]),
    Typed = Table.TransformColumnTypes(Headers, {{"AccountID", type text}, {"Customer", type text}, {"Region", type text}, {"Segment", type text}, {"Salesperson", type text}}, "en-US")
in
    Typed
