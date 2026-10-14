# Handout-only challenge: no build or server, just the video players download
# (served from publish/ at /files/...).
#
# OldFavorites.mp4 is 315 MB and already compressed (xz gains nothing), so it
# is stored as-is but split into parts under 50 MB to fit in git; the parts are
# joined here at publish time and the whole .mp4 is published.
OLDFAVORITES_PARTS := $(sort $(wildcard $(DIR)/attachments/OldFavorites.mp4.part-*))

$(BUILD_DIR)/OldFavorites.mp4: $(OLDFAVORITES_PARTS)
	$(_V)echo "Joining $(@F) from $(words $^) parts"
	$(_v)mkdir -p $(@D) && cat $^ > $@

PUBLISH_BUILD := OldFavorites.mp4
