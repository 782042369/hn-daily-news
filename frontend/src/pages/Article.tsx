import { useEffect, useState } from 'react'
import { useParams, Link } from 'react-router-dom'
import { format, parseISO } from 'date-fns'
import { zhCN } from 'date-fns/locale'
import MarkdownRenderer from '../components/MarkdownRenderer'
import Loading from '../components/Loading'

export default function Article() {
  const { date } = useParams<{ date: string }>()
  const [content, setContent] = useState<string>('')
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    if (date) {
      fetchArticle(date)
    }
  }, [date])

  const fetchArticle = async (articleDate: string) => {
    setLoading(true)
    setError(null)
    
    try {
      const response = await fetch(`./data/${articleDate}.md`)
      if (!response.ok) {
        throw new Error('文章不存在')
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
        <div className="text-6xl mb-4">🔍</div>
        <h2 className="text-2xl font-semibold text-white mb-2">未找到内容</h2>
        <p className="text-slate-400 mb-6">{error}</p>
        <Link 
          to="/" 
          className="text-orange-500 hover:text-orange-400"
        >
          返回首页
        </Link>
      </div>
    )
  }

  const formattedDate = date ? format(parseISO(date), 'yyyy年M月d日 EEEE', { locale: zhCN }) : ''

  return (
    <div>
      <div className="mb-6 flex items-center gap-4 text-sm text-slate-500">
        <Link to="/" className="hover:text-white transition-colors">首页</Link>
        <span>/</span>
        <span>{formattedDate}</span>
      </div>
      <MarkdownRenderer content={content} />
    </div>
  )
}
