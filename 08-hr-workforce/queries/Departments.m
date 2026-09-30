let
    Demo = Binary.Decompress(Binary.FromText("RctBCoUwDEXRedfyJup3B1EQhT9wBaEEDWhaYt2/IKjDC+eSZPayi5WBQG9gSpGLJgtUobNFTcTVFky8JpdANWbe5MDIznHVQA3+Wfx+jlf90KuxRflci/nMOXl50AU=", BinaryEncoding.Base64), Compression.Deflate),
    Source = if DataMode = "Demo" then Demo else if DataMode = "Folder" then File.Contents(DataFolder & "/Departments.csv") else error "DataMode must be Demo or Folder",
    Parsed = Csv.Document(Source, [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.Csv]),
    Headers = Table.PromoteHeaders(Parsed, [PromoteAllScalars=true]),
    Typed = Table.TransformColumnTypes(Headers, {{"DepartmentID", type text}, {"Department", type text}, {"Location", type text}}, "en-US")
in
    Typed
