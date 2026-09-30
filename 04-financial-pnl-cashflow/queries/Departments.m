let
    Demo = Binary.Decompress(Binary.FromText("c0ktSCwqyU3NK/F00XGBc7hcDHWCE3NSi7lcjHSCU4vKMpNBbGMdx5TczLzM4pKixJLM/DwuAA==", BinaryEncoding.Base64), Compression.Deflate),
    Source = if DataMode = "Demo" then Demo else if DataMode = "Folder" then File.Contents(DataFolder & "/Departments.csv") else error "DataMode must be Demo or Folder",
    Parsed = Csv.Document(Source, [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.Csv]),
    Headers = Table.PromoteHeaders(Parsed, [PromoteAllScalars=true]),
    Typed = Table.TransformColumnTypes(Headers, {{"DepartmentID", type text}, {"Department", type text}}, "en-US")
in
    Typed
