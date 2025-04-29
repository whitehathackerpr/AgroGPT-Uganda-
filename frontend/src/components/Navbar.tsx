import React from 'react';
import Link from 'next/link';
import { useRouter } from 'next/router';
import { useTranslation } from 'next-i18next';

const Navbar: React.FC = () => {
  const router = useRouter();
  const { t, i18n } = useTranslation();

  const changeLanguage = (lng: string) => {
    i18n.changeLanguage(lng);
  };

  const navLinks = [
    { href: '/', label: 'home' },
    { href: '/disease', label: 'disease_diagnosis' },
    { href: '/weather', label: 'weather' },
    { href: '/market', label: 'market_prices' },
    { href: '/tips', label: 'farming_tips' },
  ];

  const languages = [
    { code: 'en', label: 'EN' },
    { code: 'lg', label: 'LG' },
    { code: 'nyn', label: 'NYN' },
    { code: 'ach', label: 'ACH' },
  ];

  return (
    <header className="bg-green-600 text-white">
      <div className="container mx-auto px-4 py-4">
        <div className="flex justify-between items-center">
          <Link href="/" className="text-2xl font-bold">
            AgroGPT Uganda
          </Link>
          
          {/* Language Selector */}
          <div className="flex space-x-2">
            {languages.map((lang) => (
              <button
                key={lang.code}
                onClick={() => changeLanguage(lang.code)}
                className={`px-3 py-1 rounded ${
                  i18n.language === lang.code ? 'bg-white text-green-600' : 'hover:bg-green-500'
                }`}
              >
                {lang.label}
              </button>
            ))}
          </div>
        </div>
        
        {/* Navigation */}
        <nav className="mt-4">
          <ul className="flex space-x-6">
            {navLinks.map((link) => (
              <li key={link.href}>
                <Link
                  href={link.href}
                  className={`hover:text-green-200 ${
                    router.pathname === link.href ? 'font-bold' : ''
                  }`}
                >
                  {t(link.label)}
                </Link>
              </li>
            ))}
          </ul>
        </nav>
      </div>
    </header>
  );
};

export default Navbar; 