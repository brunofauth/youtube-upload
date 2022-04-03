complete --command=yt_upload --exclusive --short-option=t, --long-option=title --description="defaults to the video's basename"
complete --command=yt_upload --exclusive --short-option=g, --long-option=genre --description="tag the video as 'GENRE'; see '-G'"
complete --command=yt_upload --exclusive --short-option=d, --long-option=description --description="set the video's description"
complete --command=yt_upload --exclusive --short-option=p, --long-option=playlist --description="add video to PLAYLIST, creating it if needed"
complete --command=yt_upload --exclusive --short-option=T, --long-option=tag --description="tag the vide as 'TAG'; may be used many times"
complete --command=yt_upload --exclusive --short-option=D, --long-option=date-to-publish --description="formatted like '%Y-%m-%d %H:%M:%S'"
complete --command=yt_upload --exclusive --short-option=r, --long-option=recording-date --description="formatted like '%Y-%m-%d %H:%M:%S'"
complete --command=yt_upload --exclusive --short-option=l, --long-option=language --description="ISO 639-1: <en|fr|de|pt|...>"
complete --command=yt_upload --exclusive --short-option=a, --long-option=audio-language --description="ISO 639-1: <en|fr|de|pt|...>"
complete --command=yt_upload --exclusive --short-option=e, --long-option=embeddable --description="make video is embeddable"
complete --command=yt_upload --exclusive --short-option=S, --long-option=client-secrets-pass --description="client secrets entry in 'pass'"
complete --command=yt_upload --exclusive --short-option=C, --long-option=credentials-pass --description="credentials entry in 'pass'"

complete --command=yt_upload --short-option=G, --long-option=list-genres --description="list available genres and exit" \
    --arguments=(yt_upload -G)
complete --command=yt_upload --exclusive --short-option=L, --long-option=license --description="[youtube|creativeCommon]" \
    --arguments="youtube creativeCommon"
complete --command=yt_upload --exclusive --short-option=V, --long-option=visibility --description="[public|unlisted|private]" \
    --arguments="public unlisted private"

complete --command=yt_upload --require-parameter --short-option=s, --long-option=client-secrets-file --description="Secrets JSON file"
complete --command=yt_upload --require-parameter --short-option=c, --long-option=credentials-file --description="Credentials JSON file"
complete --command=yt_upload --require-parameter --short-option=n, --long-option=thumbnail --description="path to a .jpg or .png"

complete --command=yt_upload --long-option=chunksize          --exclusive --description="Bytes to send at a time, as integer"
complete --command=yt_upload --long-option=location-latitude  --exclusive --description="latitude of video recording, as float"
complete --command=yt_upload --long-option=location-longitude --exclusive --description="longitude of video recording, as float"
complete --command=yt_upload --long-option=location-altitude  --exclusive --description="altitude of video recording, as float"

complete --command=yt_upload --long-option=version --description="show the version and exit"
complete --command=yt_upload --long-option=help --description="Show a help message and exit"

