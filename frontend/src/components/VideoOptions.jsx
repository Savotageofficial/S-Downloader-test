function formatSize(bytes) {
  if (!bytes) return '';
  if (bytes < 1024) return bytes + ' B';
  if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
  if (bytes < 1024 * 1024 * 1024) return (bytes / (1024 * 1024)).toFixed(1) + ' MB';
  return (bytes / (1024 * 1024 * 1024)).toFixed(2) + ' GB';
}

function VideoOptions({ data, onBack }) {
  return (
    <div className="results-page">
      <button className="back-btn" onClick={onBack}>
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
          <line x1="19" y1="12" x2="5" y2="12" />
          <polyline points="12 19 5 12 12 5" />
        </svg>
        <span>Back</span>
      </button>

      <div className="video-header">
        {data.thumbnail && (
          <div className="video-thumbnail-wrapper">
            <img className="video-thumbnail" src={data.thumbnail} alt={data.title} />
          </div>
        )}
        <h2 className="video-title">{data.title}</h2>
      </div>

      <div className="options-grid">
        {/* Video Streams */}
        <div className="glass-card">
          <div className="card-header">
            <span className="card-icon">🎬</span>
            <h3>Video</h3>
          </div>
          <div className="stream-list">
            {data.resolutions && data.resolutions.length > 0 ? (
              data.resolutions.map((stream, i) => (
                <div className="stream-item" key={i}>
                  <div className="stream-info">
                    <span className="resolution-badge">{stream.resolution}</span>
                    {!stream.is_progressive && <span className="no-audio-badge">No Audio</span>}
                    {stream.filesize && <span className="filesize">{formatSize(stream.filesize)}</span>}
                  </div>
                  <button
                    className="download-btn"
                    onClick={() => window.open(stream.url, '_blank')}
                  >
                    Download
                  </button>
                </div>
              ))
            ) : (
              <p style={{ padding: '20px', color: 'var(--text-muted)', textAlign: 'center' }}>
                No video streams available
              </p>
            )}
          </div>
        </div>

        {/* Audio Streams */}
        <div className="glass-card">
          <div className="card-header">
            <span className="card-icon">🎵</span>
            <h3>Audio</h3>
          </div>
          <div className="stream-list">
            {data.audio && data.audio.length > 0 ? (
              data.audio.map((stream, i) => (
                <div className="stream-item" key={i}>
                  <div className="stream-info">
                    <span className="resolution-badge">{stream.abr}</span>
                    {stream.filesize && <span className="filesize">{formatSize(stream.filesize)}</span>}
                  </div>
                  <button
                    className="download-btn"
                    onClick={() => window.open(stream.url, '_blank')}
                  >
                    Download
                  </button>
                </div>
              ))
            ) : (
              <p style={{ padding: '20px', color: 'var(--text-muted)', textAlign: 'center' }}>
                No audio streams available
              </p>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default VideoOptions
