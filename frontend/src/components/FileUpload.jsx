import { useCallback, useState } from 'react';
import { useDropzone } from 'react-dropzone';
import { Upload, FileText, X, AlertCircle } from 'lucide-react';

const DEFAULT_ACCEPT = {
  'text/plain': ['.txt'],
  'application/pdf': ['.pdf'],
};

const FileUpload = ({
  onFileSelect,
  error,
  loading,
  accept = DEFAULT_ACCEPT,
  title = 'Dosya Yükle',
  emptyDescription,
  fileHint = 'Maksimum dosya boyutu: 10MB',
  variant = 'default',
  invalidTypeMessage = 'Bu dosya türü kabul edilmiyor',
}) => {
  const [selectedFile, setSelectedFile] = useState(null);

  const onDrop = useCallback(
    (acceptedFiles, rejectedFiles) => {
      if (rejectedFiles.length > 0) {
        const rejection = rejectedFiles[0];
        if (rejection.errors[0]?.code === 'file-invalid-type') {
          onFileSelect(null, invalidTypeMessage);
        } else if (rejection.errors[0]?.code === 'file-too-large') {
          onFileSelect(null, 'Dosya boyutu maksimum 10MB olabilir');
        }
        return;
      }

      if (acceptedFiles.length > 0) {
        const file = acceptedFiles[0];
        setSelectedFile(file);
        onFileSelect(file);
      }
    },
    [onFileSelect, invalidTypeMessage]
  );

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept,
    maxFiles: 1,
    maxSize: 10 * 1024 * 1024,
    disabled: loading,
  });

  const removeFile = () => {
    setSelectedFile(null);
    onFileSelect(null);
  };

  const defaultEmptyDescription =
    'Dosyanızı sürükleyip bırakın veya seçmek için tıklayın';

  return (
    <div className={`file-upload ${variant === 'compact' ? 'file-upload--compact' : ''}`}>
      <div
        {...getRootProps()}
        className={`dropzone ${variant === 'compact' ? 'dropzone--compact' : ''} ${isDragActive ? 'active' : ''} ${loading ? 'disabled' : ''}`}
      >
        <input {...getInputProps()} />

        {selectedFile ? (
          <div className="file-selected">
            <div className="file-icon">
              <FileText size={24} />
            </div>
            <div className="file-info">
              <p className="file-name">{selectedFile.name}</p>
              <p className="file-size">{(selectedFile.size / 1024).toFixed(2)} KB</p>
            </div>
            {!loading && (
              <button
                onClick={(e) => {
                  e.stopPropagation();
                  removeFile();
                }}
                className="remove-file"
                aria-label="Dosyayı kaldır"
              >
                <X size={20} />
              </button>
            )}
          </div>
        ) : (
          <div className="dropzone-content">
            <div className="upload-icon">
              <Upload size={variant === 'compact' ? 28 : 32} />
            </div>
            <h3>{title}</h3>
            <p>
              {isDragActive ? 'Dosyayı buraya bırakın...' : emptyDescription ?? defaultEmptyDescription}
            </p>
            <p className="file-hint">{fileHint}</p>
          </div>
        )}
      </div>

      {error && (
        <div className="error-message">
          <AlertCircle size={20} />
          <span>{error}</span>
        </div>
      )}
    </div>
  );
};

export default FileUpload;
