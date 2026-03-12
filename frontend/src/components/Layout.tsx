import { Outlet, Link } from 'react-router-dom'

export default function Layout() {
  return (
    <div className="min-h-screen bg-slate-900">
      {/* Header */}
      <header className="sticky top-0 z-50 bg-slate-900/95 backdrop-blur border-b border-slate-800">
        <div className="max-w-5xl mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <Link to="/" className="flex items-center gap-3">
              <span className="text-2xl">📰</span>
              <div>
                <h1 className="text-xl font-bold text-white">HN每日新闻</h1>
                <p className="text-xs text-slate-500">程序员技术资讯精选</p>
              </div>
            </Link>
            <nav className="flex items-center gap-4">
              <Link 
                to="/" 
                className="text-slate-400 hover:text-white transition-colors"
              >
                今日
              </Link>
              <Link 
                to="/archive" 
                className="text-slate-400 hover:text-white transition-colors"
              >
                归档
              </Link>
              <a 
                href="https://github.com/782042369/hn-daily-news"
                target="_blank"
                rel="noopener noreferrer"
                className="text-slate-400 hover:text-white transition-colors"
              >
                GitHub
              </a>
            </nav>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-5xl mx-auto px-4 py-8">
        <Outlet />
      </main>

      {/* Footer */}
      <footer className="border-t border-slate-800 mt-16">
        <div className="max-w-5xl mx-auto px-4 py-8">
          <div className="text-center text-slate-500 text-sm">
            <p>由歪朝团队开发维护</p>
            <p className="mt-2">
              数据来源：Hacker News 热门博客
            </p>
          </div>
        </div>
      </footer>
    </div>
  )
}
