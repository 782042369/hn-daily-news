import { useEffect, useState } from 'react'
import { format } from 'date-fns'
import MarkdownRenderer from '../components/MarkdownRenderer'
import Loading from '../components/Loading'

export default function Home() {
  const [content, setContent] = useState<string>('')
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const today = format(new Date(), 'yyyy-MM-dd')
    fetchArticle(today)
  }, [])

  const fetchArticle = async (date: string) => {
    setLoading(true)
    setError(null)
    
    try {
      const response = await fetch(`./data/${date}.md`)
      if (!response.ok) {
        throw new Error('今日内容尚未更新，请稍后再来')
      }
      const text = await response.text()
      setContent(text)
    } catch (e) {
      setError(e instanceof Error ? e.message : '加载失败')
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return <Loading />
  }

  if (error) {
    return (
      <div className="text-center py-20">
        <div className="text-6xl mb-4">📭</div>
        <h2 className="text-2xl font-semibold text-white mb-2">暂无内容</h2>
        <p className="text-slate-400 mb-6">{error}</p>
        <p className="text-slate-500 text-sm">
          每天北京时间 8:00 更新
        </p>
      </div>
    )
  }

  return (
    <div>
      <MarkdownRenderer content={content} />
    </div>
  )
}
