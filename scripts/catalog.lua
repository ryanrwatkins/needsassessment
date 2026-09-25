-- Insert generated catalog after the pre-render hook, including on a clean clone.
function Div(element)
  if element.identifier == "csv-catalog" then
    local file, message = io.open("_catalog.html", "r")
    if not file then error("Catalog generation failed: " .. message) end
    local content = file:read("*a")
    file:close()
    return pandoc.RawBlock("html", content)
  end
end
