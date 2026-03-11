import React, { useState, useEffect } from 'react'
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom'
import ReactMarkdown from 'react-markdown'
import axios from 'axios'
import dayjs from 'dayjs'
import './styles/index.css'

function App() {
  const [darkMode, setDarkMode] = useState(false)

  useEffect(() => {
    if (darkMode) {
      document.documentElement.classList.add('dark')
    } else {
      document.documentElement.classList.remove('dark')
    }
  }, [darkMode])

  return (
    <Router basename="/hn-daily-news">
      <div className="min-h-screen bg-gray-50 dark:bg-gray-900 transition-colors duration-200">
        <header className="bg-white dark:bg-gray-800 shadow-sm sticky top-0 z-50">
          <div className="max-w-4xl mx-auto px-4 py-4 flex justify-between items-center">
            <Link to="/" className="flex items-center space-x-2">
              <span className="text-2xl">📰</span>
              <h1 className="text-xl font-bold text-gray-900 dark:text-white">HN每日新闻</h1>
            </Link>
            <button
              onClick={() => setDarkMode(!darkMode)}
              className="p-2 rounded-lg bg-gray-200 dark:bg-gray-700 hover:bg-gray-300 dark:hover:bg-gray-600 transition-colors"
            >
              {darkMode ? '☀️' : '🌙'}
            </button>
          </div>
        </header>

        <main className="max-w-4xl mx-auto px-4 py-8">
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/news/:date" element={<NewsPage />} />
            <Route path="/history" element={<HistoryPage />} />
          </Routes>
        </main>

        <footer className="bg-white dark:bg-gray-800 border-t border-gray-200 dark:border-gray-700 mt-12">
          <div className="max-w-4xl mx-auto px-4 py-6 text-center text-gray-600 dark:text-gray-400 text-sm">
            <p>为程序员精选的每日技术热点 | 自动抓取 · AI摘要 · 每日更新</p>
            <p className="mt-2">
              <a href="https://github.com/782042369/hn-daily-news" 
                 className="text-blue-500 hover:text-blue-600 dark:text-blue-400">
                GitHub
              </a>
            </p>
          </div>
        </footer>
      </div>
    </Router>
  )
}

function HomePage() {
  const today = dayjs().format('YYYY-MM-DD')
  return (
    <div>
      <div className="text-center mb-8">
        <h2 className="text-3xl font-bold text-gray-900 dark:text-white mb-4">
          今日新闻
        </h2>
        <p className="text-gray-600 dark:text-gray-400">
          {dayjs().format('YYYY年MM月DD日')}
        </p>
      </div>
      <NewsPage date={today} />
      <div className="mt-8 text-center">
        <Link 
          to="/history" 
          className="text-blue-500 hover:text-blue-600 dark:text-blue-400 font-medium"
        >
          查看历史新闻 →
        </Link>
      </div>
    </div>
  )
}

function NewsPage({ date }) {
  const [content, setContent] = useState('')
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    const fetchNews = async () => {
      try {
        setLoading(true)
        const response = await axios.get(
          `https://raw.githubusercontent.com/782042369/hn-daily-news/main/data/news/hn-daily-${date}.md`
        )
        setContent(response.data)
        setError(null)
      } catch (err) {
        setError('暂无该日期的新闻')
        setContent('')
      } finally {
        setLoading(false)
      }
    }

    fetchNews()
  }, [date])

  if (loading) {
    return (
      <div className="flex justify-center items-center py-12">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="text-center py-12">
        <p className="text-gray-600 dark:text-gray-400">{error}</p>
      </div>
    )
  }

  return (
    <article className="prose prose-lg dark:prose-invert max-w-none">
      <ReactMarkdown>{content}</ReactMarkdown>
    </article>
  )
}

function HistoryPage() {
  const [dates, setDates] = useState([])
  
  useEffect(() => {
    // 生成最近7天的日期列表
    const recentDates = []
    for (let i = 0; i < 7; i++) {
      recentDates.push(dayjs().subtract(i, 'day').format('YYYY-MM-DD'))
    }
    setDates(recentDates)
  }, [])

  return (
    <div>
      <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-6">历史新闻</h2>
      <div className="space-y-4">
        {dates.map(date => (
          <Link
            key={date}
            to={`/news/${date}`}
            className="block bg-white dark:bg-gray-800 rounded-lg p-4 shadow-sm hover:shadow-md transition-shadow"
          >
            <div className="flex justify-between items-center">
              <div>
                <p className="font-medium text-gray-900 dark:text-white">
                  {dayjs(date).format('YYYY年MM月DD日')}
                </p>
                <p className="text-sm text-gray-600 dark:text-gray-400">
                  {dayjs(date).format('dddd')}
                </p>
              </div>
              <span className="text-blue-500">→</span>
            </div>
          </Link>
        ))}
      </div>
    </div>
  )
}

export default App
