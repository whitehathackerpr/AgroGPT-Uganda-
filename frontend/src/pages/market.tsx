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

const MarketPrices: React.FC = () => {
  const { t } = useTranslation();
  const [selectedCrop, setSelectedCrop] = useState('maize');
  const [selectedRegion, setSelectedRegion] = useState('central');

  const fetchMarketData = async () => {
    const response = await axios.get(
      `/api/market-prices?crop=${selectedCrop}&region=${selectedRegion}`
    );
    return response.data;
  };

  const { data, isLoading, error } = useQuery(
    ['market', selectedCrop, selectedRegion],
    fetchMarketData,
    {
      enabled: !!selectedCrop && !!selectedRegion,
    }
  );

  const chartData = {
    labels: data?.insights.current_prices.map((price: any) => price.date) || [],
    datasets: [
      {
        label: t('price_trend'),
        data: data?.insights.price_trend.predicted_prices || [],
        borderColor: 'rgb(75, 192, 192)',
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
        text: t('price_trend'),
      },
    },
  };

  return (
    <Layout>
      <div className="max-w-4xl mx-auto">
        <h1 className="text-3xl font-bold mb-8">{t('market_prices')}</h1>

        <div className="bg-white rounded-lg shadow-md p-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                {t('select_crop')}
              </label>
              <select
                value={selectedCrop}
                onChange={(e) => setSelectedCrop(e.target.value)}
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-green-500 focus:ring-green-500"
              >
                <option value="maize">Maize</option>
                <option value="beans">Beans</option>
                <option value="coffee">Coffee</option>
                <option value="bananas">Bananas</option>
                <option value="cassava">Cassava</option>
              </select>
            </div>

            <div>
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
              <div className="mb-8">
                <h2 className="text-xl font-semibold mb-4">{t('current_prices')}</h2>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                  {data?.insights.current_prices.map((price: any) => (
                    <div
                      key={price.date}
                      className="bg-gray-50 p-4 rounded-lg"
                    >
                      <div className="flex justify-between items-center">
                        <span className="font-medium">{price.date}</span>
                        <span className="text-green-600 font-bold">
                          {price.price} {price.unit}
                        </span>
                      </div>
                      <div className="text-sm text-gray-500 mt-2">
                        {price.source}
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              <div className="mb-8">
                <h2 className="text-xl font-semibold mb-4">{t('price_trend')}</h2>
                <div className="h-64">
                  <Line data={chartData} options={options} />
                </div>
              </div>

              <div className="bg-green-50 p-4 rounded-lg">
                <h2 className="text-xl font-semibold mb-2">{t('recommendation')}</h2>
                <p className="text-gray-700">{data?.insights.recommendation}</p>
              </div>
            </>
          )}
        </div>
      </div>
    </Layout>
  );
};

export default MarketPrices; 