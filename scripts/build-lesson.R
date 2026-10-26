# The chapter template opens a whisker section on `progress`. A length-1
# character such as "0", or NA, becomes the section context and the next
# lookup throws. Drop the bar so the page can render.
local({
  trace(
    sandpaper:::build_episode_html,
    quote({
      page_progress <- NULL
    }),
    print = FALSE
  )
})
options(warn = 1)
sandpaper::build_lesson(quiet = FALSE, preview = FALSE)
