-- Drop blocks that belong to the other target.
-- WORKBENCH_TARGET=site drops slides-only material.
-- WORKBENCH_TARGET=slides drops site-only material, solutions, and raw HTML.
-- Figures are images, and this filter does not remove images.

local function drop_class(el, name)
  return el.t == "Div" and el.classes:includes(name)
end

function Div(el)
  local target = os.getenv("WORKBENCH_TARGET") or "site"
  if target == "site" and drop_class(el, "slidesonly") then
    return {}
  end
  if target == "slides" and (drop_class(el, "siteonly") or drop_class(el, "solution")) then
    return {}
  end
  return nil
end

function RawBlock(el)
  local target = os.getenv("WORKBENCH_TARGET") or "site"
  if target == "slides" and el.format == "html" then
    return {}
  end
  return nil
end
