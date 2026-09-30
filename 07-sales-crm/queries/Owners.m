let
    Demo = Binary.Decompress(Binary.FromText("8y/PSy3ydNHxB9E6IamJuVxBhjqOKWWZxflFCoY6rnklqUUFRZnFqVxBRnBxI52AxKISoI5iriBjuKixjmdeUn5pXgpXkAlc0ATFCFO4uCmSEWZwUTOEEeZwQXMUIyzg4hZIRljCRS3hRgAA", BinaryEncoding.Base64), Compression.Deflate),
    Source = if DataMode = "Demo" then Demo else if DataMode = "Folder" then File.Contents(DataFolder & "/Owners.csv") else error "DataMode must be Demo or Folder",
    Parsed = Csv.Document(Source, [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.Csv]),
    Headers = Table.PromoteHeaders(Parsed, [PromoteAllScalars=true]),
    Typed = Table.TransformColumnTypes(Headers, {{"OwnerID", type text}, {"Owner", type text}, {"Team", type text}}, "en-US")
in
    Typed
