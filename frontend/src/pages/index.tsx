import React from 'react';
import { useTranslation } from 'next-i18next';
import { serverSideTranslations } from 'next-i18next/serverSideTranslations';
import Layout from '../components/Layout';

export default function Home() {
  const { t } = useTranslation();

  const features = [
    {
      icon: '🌱',
      title: 'disease_diagnosis',
      description: 'disease_diagnosis_description',
    },
    {
      icon: '☀️',
      title: 'weather_forecast',
      description: 'weather_forecast_description',
    },
    {
      icon: '💰',
      title: 'market_prices',
      description: 'market_prices_description',
    },
    {
      icon: '📱',
      title: 'sms_support',
      description: 'sms_support_description',
    },
  ];

  return (
    <Layout>
      {/* Hero Section */}
      <section className="text-center py-12 px-4">
        <h1 className="text-4xl md:text-6xl font-bold text-gray-900 mb-4">
          {t('hero_title')}
        </h1>
        <p className="text-xl text-gray-600 mb-8 max-w-2xl mx-auto">
          {t('hero_description')}
        </p>
        <button className="bg-green-600 text-white px-8 py-3 rounded-lg text-lg font-semibold hover:bg-green-700 transition-colors">
          {t('get_started')}
        </button>
      </section>

      {/* Features Grid */}
      <section className="py-12">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
          {features.map((feature) => (
            <div
              key={feature.title}
              className="bg-white p-6 rounded-lg shadow-md hover:shadow-lg transition-shadow"
            >
              <div className="text-4xl mb-4">{feature.icon}</div>
              <h3 className="text-xl font-semibold mb-2">{t(feature.title)}</h3>
              <p className="text-gray-600">{t(feature.description)}</p>
            </div>
          ))}
        </div>
      </section>

      {/* CTA Section */}
      <section className="bg-green-50 py-12 px-4 rounded-lg text-center mt-12">
        <h2 className="text-3xl font-bold text-gray-900 mb-4">
          {t('cta_title')}
        </h2>
        <p className="text-xl text-gray-600 mb-8 max-w-2xl mx-auto">
          {t('cta_description')}
        </p>
        <div className="flex justify-center space-x-4">
          <button className="bg-green-600 text-white px-6 py-2 rounded-lg font-semibold hover:bg-green-700 transition-colors">
            {t('register_now')}
          </button>
          <button className="border-2 border-green-600 text-green-600 px-6 py-2 rounded-lg font-semibold hover:bg-green-50 transition-colors">
            {t('learn_more')}
          </button>
        </div>
      </section>
    </Layout>
  );
}

export async function getStaticProps({ locale }: { locale: string }) {
  return {
    props: {
      ...(await serverSideTranslations(locale, ['common'])),
    },
  };
} 