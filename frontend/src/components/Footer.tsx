import React from 'react';
import Link from 'next/link';
import { useTranslation } from 'next-i18next';

const Footer: React.FC = () => {
  const { t } = useTranslation();

  const quickLinks = [
    { href: '/contact', label: 'contact_us' },
    { href: '/privacy', label: 'privacy_policy' },
    { href: '/terms', label: 'terms_of_service' },
  ];

  return (
    <footer className="bg-gray-800 text-white mt-8">
      <div className="container mx-auto px-4 py-6">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div>
            <h3 className="text-lg font-bold mb-4">{t('about_us')}</h3>
            <p className="text-gray-300">
              {t('about_description')}
            </p>
          </div>
          <div>
            <h3 className="text-lg font-bold mb-4">{t('quick_links')}</h3>
            <ul className="space-y-2">
              {quickLinks.map((link) => (
                <li key={link.href}>
                  <Link href={link.href} className="text-gray-300 hover:text-white">
                    {t(link.label)}
                  </Link>
                </li>
              ))}
            </ul>
          </div>
          <div>
            <h3 className="text-lg font-bold mb-4">{t('contact_info')}</h3>
            <ul className="space-y-2 text-gray-300">
              <li>Email: info@agrogpt-uganda.com</li>
              <li>Phone: +256 XXX XXX XXX</li>
              <li>Address: Kampala, Uganda</li>
            </ul>
          </div>
        </div>
        <div className="mt-8 pt-8 border-t border-gray-700 text-center text-gray-300">
          <p>&copy; {new Date().getFullYear()} AgroGPT Uganda. {t('all_rights_reserved')}</p>
        </div>
      </div>
    </footer>
  );
};

export default Footer; 