--[[
  chord_dataset_browser.lua
  ReaImGui panel to browse chord progression index in REAPER
]]

-- Determine script folder and load generated index
local script_path = debug.getinfo(1, "S").source:sub(2):match("(.+[/\\])") or ""
local index_file = script_path .. "chord_dataset_index.lua"
-- load generated index; CHORD_INDEX should be defined by this file
CHORD_INDEX = CHORD_INDEX or {}
local ok, err = pcall(dofile, index_file)
if not ok then
  reaper.ShowMessageBox("Failed to load chord index: " .. tostring(err), "Error", 0)
  return
end

-- Create ImGui context
local ctx = reaper.ImGui_CreateContext("Chord Dataset Browser")

-- Pagination state
local page = 1
local items_per_page = 10

function draw()
  local visible, open = reaper.ImGui_Begin(ctx, "Chord Dataset Browser", true)
  if visible then
    local total = #CHORD_INDEX
    local total_pages = math.ceil(total / items_per_page)
    reaper.ImGui_Text(ctx, string.format("Page %d / %d", page, total_pages))

    if reaper.ImGui_Button(ctx, "Prev") then
      if page > 1 then page = page - 1 end
    end
    reaper.ImGui_SameLine(ctx)
    if reaper.ImGui_Button(ctx, "Next") then
      if page < total_pages then page = page + 1 end
    end

    reaper.ImGui_SameLine(ctx)
    reaper.ImGui_Text(ctx, "Items per page:")
    reaper.ImGui_SameLine(ctx)
    local changed, val = reaper.ImGui_InputInt(ctx, "##items", items_per_page, 0)
    if changed and val > 0 then
      items_per_page = val
      page = 1 -- reset to first page
    end

    -- Display entries as simple text list
    local start_idx = (page - 1) * items_per_page + 1
    local end_idx = math.min(total, page * items_per_page)
    for i = start_idx, end_idx do
      local entry = CHORD_INDEX[i]
      if entry then
        reaper.ImGui_Text(ctx, string.format("%3d: %s", entry.id, table.concat(entry.chords, " ")))
      end
    end

    reaper.ImGui_End(ctx)
  end

  if open then
    reaper.defer(draw)
  else
    reaper.ImGui_DestroyContext(ctx)
  end
end

-- Launch the UI
draw()
