root = hd(System.argv())
for path <- Path.wildcard(Path.join(root, "*.beam")) do
  IO.puts("FILE #{Path.basename(path)}")
  IO.inspect(:beam_lib.chunks(String.to_charlist(path), [:compile_info]), limit: 10)
  result = :beam_disasm.file(String.to_charlist(path))
  File.write!(path <> ".disasm.txt", inspect(result, pretty: true, limit: :infinity, printable_limit: :infinity, width: 140))
end
