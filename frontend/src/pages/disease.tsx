import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';
import Layout from '../components/Layout';
import { useQuery } from 'react-query';
import axios from 'axios';

const DiseaseDiagnosis: React.FC = () => {
  const { t } = useTranslation();
  const [selectedImage, setSelectedImage] = useState<File | null>(null);
  const [description, setDescription] = useState('');
  const [cropType, setCropType] = useState('');
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const handleImageUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files && event.target.files[0]) {
      setSelectedImage(event.target.files[0]);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    try {
      const formData = new FormData();
      if (selectedImage) {
        formData.append('image', selectedImage);
      }
      formData.append('description', description);
      formData.append('crop_type', cropType);

      const response = await axios.post('/api/diagnose-disease', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      setResult(response.data);
    } catch (error) {
      console.error('Error diagnosing disease:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Layout>
      <div className="max-w-4xl mx-auto">
        <h1 className="text-3xl font-bold mb-8">{t('disease_diagnosis')}</h1>
        
        <div className="bg-white rounded-lg shadow-md p-6">
          <form onSubmit={handleSubmit} className="space-y-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                {t('upload_image')}
              </label>
              <input
                type="file"
                accept="image/*"
                onChange={handleImageUpload}
                className="block w-full text-sm text-gray-500
                  file:mr-4 file:py-2 file:px-4
                  file:rounded-full file:border-0
                  file:text-sm file:font-semibold
                  file:bg-green-50 file:text-green-700
                  hover:file:bg-green-100"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                {t('crop_type')}
              </label>
              <select
                value={cropType}
                onChange={(e) => setCropType(e.target.value)}
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-green-500 focus:ring-green-500"
                required
              >
                <option value="">{t('select_crop')}</option>
                <option value="maize">Maize</option>
                <option value="beans">Beans</option>
                <option value="coffee">Coffee</option>
                <option value="bananas">Bananas</option>
                <option value="cassava">Cassava</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                {t('description')}
              </label>
              <textarea
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                rows={4}
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-green-500 focus:ring-green-500"
                placeholder={t('describe_symptoms')}
              />
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full bg-green-600 text-white py-2 px-4 rounded-md hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-offset-2 disabled:opacity-50"
            >
              {loading ? t('analyzing') : t('diagnose')}
            </button>
          </form>

          {result && (
            <div className="mt-8 p-4 bg-gray-50 rounded-lg">
              <h2 className="text-xl font-semibold mb-4">{t('diagnosis_result')}</h2>
              <div className="space-y-4">
                <div>
                  <span className="font-medium">{t('disease')}:</span>
                  <span className="ml-2">{result.disease}</span>
                </div>
                <div>
                  <span className="font-medium">{t('confidence')}:</span>
                  <span className="ml-2">{Math.round(result.confidence * 100)}%</span>
                </div>
                <div>
                  <h3 className="font-medium mb-2">{t('symptoms')}:</h3>
                  <p className="text-gray-600">{result.information.symptoms}</p>
                </div>
                <div>
                  <h3 className="font-medium mb-2">{t('treatment')}:</h3>
                  <p className="text-gray-600">{result.information.treatment}</p>
                </div>
                <div>
                  <h3 className="font-medium mb-2">{t('prevention')}:</h3>
                  <p className="text-gray-600">{result.information.prevention}</p>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </Layout>
  );
};

export default DiseaseDiagnosis; 