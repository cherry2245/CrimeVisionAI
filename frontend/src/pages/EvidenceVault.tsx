import { useState } from 'react'
import { Upload, FileText, Trash2 } from 'lucide-react'

const EvidenceVault = () => {
  const [evidenceList, setEvidenceList] = useState<any[]>([])
  const [uploading, setUploading] = useState(false)

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (!file) return

    setUploading(true)
    const formData = new FormData()
    formData.append('file', file)

    try {
      const response = await fetch('http://127.0.0.1:5000/api/v1/evidence/upload', {
        method: 'POST',
        body: formData,
      })
      const data = await response.json()
      if (response.ok) {
        setEvidenceList([...evidenceList, data])
      } else {
        alert(data.error || 'Upload failed')
      }
    } catch (error) {
      alert('Upload failed: ' + error)
    } finally {
      setUploading(false)
    }
  }

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-white">Evidence Vault</h1>

      {/* Upload Section */}
      <div className="bg-navy-800 rounded-lg border border-gray-700 p-6">
        <h2 className="text-lg font-semibold text-white mb-4">Upload Evidence</h2>
        <div className="flex items-center gap-4">
          <input
            type="file"
            accept="image/*"
            onChange={handleFileUpload}
            disabled={uploading}
            className="flex-1 text-sm text-gray-400 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-semibold file:bg-cyan-600 file:text-white hover:file:bg-cyan-700"
          />
          {uploading && <span className="text-gray-400">Uploading...</span>}
        </div>
      </div>

      {/* Evidence List */}
      <div className="bg-navy-800 rounded-lg border border-gray-700 p-6">
        <h2 className="text-lg font-semibold text-white mb-4">Evidence Items</h2>
        {evidenceList.length === 0 ? (
          <p className="text-gray-400">No evidence uploaded yet</p>
        ) : (
          <div className="space-y-2">
            {evidenceList.map((item) => (
              <div key={item.evidence_id} className="flex/items-center justify-between p-3 bg-navy-700 rounded-lg">
                <div className="flex items-center gap-3">
                  <FileText className="w-5 h-5 text-cyan-500" />
                  <div>
                    <p className="text-white text-sm">{item.original_filename}</p>
                    <p className="text-gray-400 text-xs">{item.file_size} bytes</p>
                  </div>
                </div>
                <span className={`text-xs px-2 py-1 rounded ${
                  item.processing_status === 'analyzed' ? 'bg-green-600 text-white' : 'bg-yellow-600 text-white'
                }`}>
                  {item.processing_status}
                </span>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}

export default EvidenceVault
