-- Workbench and Beamer tweaks for Org sources.
-- Markdown: plain code, nested solutions, real output blocks, no raw TeX.
-- Beamer: slide figures are the PNG renders.

function Code(el)
  if FORMAT:match("markdown") then
    return pandoc.Code(el.text)
  end
  return nil
end

function CodeBlock(el)
  if not FORMAT:match("markdown") then
    return nil
  end
  -- Org records the source language twice. Pegboard cannot parse the attribute.
  el.attributes["org-language"] = nil
  local lang = el.classes[1]
  if lang == "bash" or lang == "sh" or lang == "shell" then
    lang = "bash"
  end
  if lang == nil then
    return pandoc.CodeBlock(el.text)
  end
  return pandoc.CodeBlock(el.text, pandoc.Attr("", {lang}, {}))
end

local function inlines_to_text(inlines)
  local parts = {}
  for _, item in ipairs(inlines) do
    if item.t == "Str" or item.t == "Code" then
      table.insert(parts, item.text)
    elseif item.t == "Space" then
      table.insert(parts, " ")
    elseif item.t == "SoftBreak" or item.t == "LineBreak" then
      table.insert(parts, "\n")
    end
  end
  return table.concat(parts)
end

function Div(el)
  if FORMAT:match("markdown") and el.classes:includes("output") then
    local chunks = {}
    for _, block in ipairs(el.content) do
      if block.t == "CodeBlock" then
        table.insert(chunks, block.text)
      elseif block.t == "Para" or block.t == "Plain" then
        table.insert(chunks, inlines_to_text(block.content))
      end
    end
    return pandoc.CodeBlock(table.concat(chunks, "\n") .. "\n")
  end
  return nil
end

function RawBlock(el)
  if FORMAT:match("markdown") and (el.format == "latex" or el.format == "tex") then
    return {}
  end
  return nil
end

function Header(el)
  if FORMAT:match("beamer") then
    el.classes:insert("allowframebreaks")
  end
  return el
end

function Image(el)
  if FORMAT:match("beamer") or FORMAT:match("latex") then
    local src = el.src:gsub("%.svg$", ".png")
    src = src:gsub("^fig/", "")
    src = src:gsub("^episodes/fig/", "")
    el.src = src
  end
  return el
end

function Pandoc(doc)
  if not FORMAT:match("markdown") then
    return doc
  end
  local out = {}
  for _, block in ipairs(doc.blocks) do
    if block.t == "Div" and block.classes:includes("solution") then
      local prev = out[#out]
      if prev and prev.t == "Div" and prev.classes:includes("challenge") then
        prev.content:insert(block)
      else
        table.insert(out, block)
      end
    else
      table.insert(out, block)
    end
  end
  doc.blocks = out
  return doc
end
