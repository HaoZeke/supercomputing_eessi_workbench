# Drop the chapter progress bar. A length-1 value becomes the whisker
# section context and the next lookup throws.
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
