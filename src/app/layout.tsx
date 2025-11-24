import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import { Analytics } from "@vercel/analytics/next";
import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: {
    default: "Gheed's Gamble - D2R Hardcore Randomizer",
    template: "%s | Gheed's Gamble"
  },
  description: "Randomize your Diablo 2 Resurrected Hardcore experience! Spin the wheel to get random class builds and challenging modifiers. Perfect for streamers and hardcore players seeking fresh gameplay.",
  keywords: ["Diablo 2", "D2R", "Diablo 2 Resurrected", "Hardcore", "Randomizer", "Build Generator", "Challenge Mode", "Gaming Tool", "Streaming Tool"],
  authors: [{ name: "Gheed's Gamble" }],
  creator: "Gheed's Gamble",
  publisher: "Gheed's Gamble",
  metadataBase: new URL('https://gheedsgamble.com'),
  alternates: {
    canonical: '/',
  },
  openGraph: {
    title: "Gheed's Gamble - D2R Hardcore Randomizer",
    description: "Randomize your Diablo 2 Resurrected Hardcore experience! Spin the wheel for random builds and challenges.",
    url: 'https://gheedsgamble.com',
    siteName: "Gheed's Gamble",
    locale: 'en_US',
    type: 'website',
    images: [
      {
        url: '/og-image.png',
        width: 1200,
        height: 630,
        alt: "Gheed's Gamble - Diablo 2 Resurrected Randomizer",
      },
    ],
  },
  twitter: {
    card: 'summary_large_image',
    title: "Gheed's Gamble - D2R Hardcore Randomizer",
    description: "Randomize your Diablo 2 Resurrected Hardcore experience! Spin the wheel for random builds and challenges.",
    images: ['/og-image.png'],
  },
  robots: {
    index: true,
    follow: true,
    googleBot: {
      index: true,
      follow: true,
      'max-video-preview': -1,
      'max-image-preview': 'large',
      'max-snippet': -1,
    },
  },
  icons: {
    icon: '/favicon.ico',
    apple: '/apple-touch-icon.png',
  },
  manifest: '/site.webmanifest',
  themeColor: '#8B0000',
  viewport: {
    width: 'device-width',
    initialScale: 1,
    maximumScale: 5,
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  const jsonLd = {
    '@context': 'https://schema.org',
    '@type': 'WebApplication',
    name: "Gheed's Gamble",
    description: 'Diablo 2 Resurrected Hardcore Randomizer - Generate random character builds and challenges',
    url: 'https://gheedsgamble.com',
    applicationCategory: 'GameApplication',
    operatingSystem: 'Web Browser',
    offers: {
      '@type': 'Offer',
      price: '0',
      priceCurrency: 'USD',
    },
    featureList: [
      'Random class selection',
      'Random build generation',
      'Challenge modifiers',
      'Run history tracking',
      'Export/Import functionality',
    ],
  };

  return (
    <html lang="en" suppressHydrationWarning>
      <head>
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
        />
      </head>
      <body className={`${geistSans.variable} ${geistMono.variable}`}>
        {children}
        <Analytics />
      </body>
    </html>
  );
}
