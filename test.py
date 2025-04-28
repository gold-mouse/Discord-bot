from utility import *
from toast_notification import show_toast

update_status("Failed to forum post - ```Missed Tag Ids```", "warning")

show_toast(
    title="🚀 Slide In Toast",
    message="This toast slides in smoothly from the screen edge.",
    position="top-center",
    toast_type="info",
    duration=4000,
    url="https://exmple.com"
)

print("Done")
