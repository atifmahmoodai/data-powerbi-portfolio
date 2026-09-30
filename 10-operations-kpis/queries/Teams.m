let
    Demo = Binary.Decompress(Binary.FromText("C0lNzPV00QkBUjo++cmJJZn5eVwhhjr+BalFYE6xAkhOwVDHJzEjvyiVK8QIQ85Ix7M4JzE3MSkxhSvEGEPaWMc7sSgxOSOTK8QEQ9IEbq4phpwpsrlmGNJmcHMB", BinaryEncoding.Base64), Compression.Deflate),
    Source = if DataMode = "Demo" then Demo else if DataMode = "Folder" then File.Contents(DataFolder & "/Teams.csv") else error "DataMode must be Demo or Folder",
    Parsed = Csv.Document(Source, [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.Csv]),
    Headers = Table.PromoteHeaders(Parsed, [PromoteAllScalars=true]),
    Typed = Table.TransformColumnTypes(Headers, {{"TeamID", type text}, {"Team", type text}, {"Location", type text}}, "en-US")
in
    Typed
