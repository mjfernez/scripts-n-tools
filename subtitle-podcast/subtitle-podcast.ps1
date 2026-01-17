<#
Usage:
  .\subtitle-podcast.ps1 episode01.mp3

Place cover files in the same directory as your mp3, with a name like "episode01.jpg" (PNG is also OK)

If a cover is not supplied, a black background will be made instead

Requirements:
  - Python in PATH
  - ffmpeg in PATH
    whispeX installed via pip
#>

param (
    [Parameter(Mandatory = $true)]
    [string]$InputAudio
)

# https://github.com/m-bain/whisperX/issues/1304#issuecomment-3599061751
$env:TORCH_FORCE_NO_WEIGHTS_ONLY_LOAD = "true"

$Title = [System.IO.Path]::GetFileNameWithoutExtension($InputAudio)

Write-Host "Processing: $InputAudio"
Write-Host "Base title: $Title"

# -----------------------------
# Run WhisperX
# ----------------------------
# https://github.com/m-bain/whisperX/issues/878
whisperx `
    --compute_type float32 `
    --model large-v2 `
    --align_model WAV2VEC2_ASR_LARGE_LV60K_960H `
    --output_format srt `
    --batch_size 4 `
    --highlight_words True `
    $InputAudio


# -----------------------------
# Create subtitled video
# -----------------------------
$OutputVideo = "$Title.mkv"

$Image = @()
if (Test-Path "$Title.jpg") {
    $Image += @("-loop", "1", "-i", "$Title.jpg")
} elseif (Test-Path "$Title.png") {
    $Image += @("-loop", "1", "-i", "$Title.png")
} else{
    Write-Warning "No image with '$Title' found, making blank background"
    $Image += @("-f", "lavfi", "-i", "color=c=black:s=1280x720")
}


ffmpeg `
    @Image `
    -i $InputAudio `
    -vf "subtitles=${Title}.srt:force_style='FontSize=28,Alignment=2'" `
    -c:a copy `
    -shortest `
    $OutputVideo

Write-Host "Done!"
Write-Host "Output: $OutputVideo"
