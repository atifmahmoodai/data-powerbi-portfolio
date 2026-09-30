let
    Demo = Binary.Decompress(Binary.FromText("hZJNbsMgFIT3OYUPwMID+CfLKMmii0qWcgJk0chVDJJDWvX2JY2wTGfB7unBJ4bRNyz+047h7SSG1ySOt8m6IN6NM1e7iItdvqbR7oa6hjjZ2Vdnd40nc7xUxdXreiUTEKeDM7efMI33JyQZkglSK6TExX+Eb7P8PaSYUYnRK6PF4RH8bMLk3ZPSTOlENSuFPF7DUJOgdvOnbbyWmTYx2Hwpj9cx1XF7Oo/XM9Rze8ji7ZnZc3syj4eaqLii9lQWD2wEwO3pbTywEJDcHv7FYyWgSu6BjYAuuAcWAk3RPbASaEvugY1AV3APLAT6gnu/", BinaryEncoding.Base64), Compression.Deflate),
    Source = if DataMode = "Demo" then Demo else if DataMode = "Folder" then File.Contents(DataFolder & "/Projects.csv") else error "DataMode must be Demo or Folder",
    Parsed = Csv.Document(Source, [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.Csv]),
    Headers = Table.PromoteHeaders(Parsed, [PromoteAllScalars=true]),
    Typed = Table.TransformColumnTypes(Headers, {{"ProjectID", type text}, {"Project", type text}, {"Client", type text}, {"Manager", type text}, {"Service", type text}}, "en-US")
in
    Typed
