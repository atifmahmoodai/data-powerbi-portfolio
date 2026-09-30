let
    Demo = Binary.Decompress(Binary.FromText("c85IzMtLzfF00XGGsHR8E4uyU0u4nA11wlOTFFIyi1KTS3QCErMzi0sS87icjaAKCnISk1ORxI11gvOTMxNzFJLzc3NTi5DlAA==", BinaryEncoding.Base64), Compression.Deflate),
    Source = if DataMode = "Demo" then Demo else if DataMode = "Folder" then File.Contents(DataFolder & "/Channels.csv") else error "DataMode must be Demo or Folder",
    Parsed = Csv.Document(Source, [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.Csv]),
    Headers = Table.PromoteHeaders(Parsed, [PromoteAllScalars=true]),
    Typed = Table.TransformColumnTypes(Headers, {{"ChannelID", type text}, {"Channel", type text}, {"Market", type text}}, "en-US")
in
    Typed
