import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';
import Layout from '../components/Layout';
import { useQuery } from 'react-query';
import axios from 'axios';
import { Line } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

const WeatherForecast: React.FC = () => {
  const { t } = useTranslation();
  const [selectedRegion, setSelectedRegion] = useState('central');
  const [forecastData, setForecastData] = useState<any>(null);

  const fetchWeatherData = async () => {
    const response = await axios.get(`/api/weather-forecast?region=${selectedRegion}`);
    return response.data;
  };

  const { data, isLoading, error } = useQuery(
    ['weather', selectedRegion],
    fetchWeatherData,
    {
      enabled: !!selectedRegion,
    }
  );

  const chartData = {
    labels: data?.forecast.map((day: any) => day.date) || [],
    datasets: [
      {
        label: t('temperature'),
        data: data?.forecast.map((day: any) => day.temperature) || [],
        borderColor: 'rgb(75, 192, 192)',
        tension: 0.1,
      },
      {
        label: t('rainfall'),
        data: data?.forecast.map((day: any) => day.rainfall) || [],
        borderColor: 'rgb(53, 162, 235)',
        tension: 0.1,
      },
    ],
  };

  const options = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top' as const,
      },
      title: {
        display: true,
        text: t('weather_forecast'),
      },
    },
  };

  return (
    <Layout>
      <div className="max-w-4xl mx-auto">
        <h1 className="text-3xl font-bold mb-8">{t('weather_forecast')}</h1>

        <div className="bg-white rounded-lg shadow-md p-6">
          <div className="mb-6">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              {t('select_region')}
            </label>
            <select
              value={selectedRegion}
              onChange={(e) => setSelectedRegion(e.target.value)}
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-green-500 focus:ring-green-500"
            >
              <option value="central">{t('central')}</option>
              <option value="eastern">{t('eastern')}</option>
              <option value="northern">{t('northern')}</option>
              <option value="western">{t('western')}</option>
            </select>
          </div>

          {isLoading ? (
            <div className="text-center py-8">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-green-600 mx-auto"></div>
              <p className="mt-4 text-gray-600">{t('loading')}</p>
            </div>
          ) : error ? (
            <div className="text-center py-8 text-red-600">
              {t('error_loading_data')}
            </div>
          ) : (
            <>
              <div className="h-64 mb-8">
                <Line data={chartData} options={options} />
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {data?.forecast.map((day: any) => (
                  <div
                    key={day.date}
                    className="bg-gray-50 p-4 rounded-lg"
                  >
                    <h3 className="font-semibold mb-2">{day.date}</h3>
                    <div className="space-y-2">
                      <div className="flex justify-between">
                        <span className="text-gray-600">{t('temperature')}:</span>
                        <span className="font-medium">{day.temperature}°C</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-gray-600">{t('rainfall')}:</span>
                        <span className="font-medium">{day.rainfall}mm</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-gray-600">{t('humidity')}:</span>
                        <span className="font-medium">{day.humidity}%</span>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </>
          )}
        </div>
      </div>
    </Layout>
  );
};

export default WeatherForecast; 