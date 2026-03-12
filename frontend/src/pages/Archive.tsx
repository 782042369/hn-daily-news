import { useEffect, useState } from 'react'
import ArticleCard from '../components/ArticleCard'
import Loading from '../components/Loading'

interface ArchiveItem {
  date: string
  title: string
  preview?: string
  articleCount?: number
}

export default function Archive() {
  const [archives, setArchives] = useState<ArchiveItem[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    // 获取归档列表（从index.json或直接遍历）
    fetchArchiveList()
  }, [])

  const fetchArchiveList = async () => {
    try {
      const response = await fetch('./data/index.json')
      if (response.ok) {
        const data = await response.json()
        setArchives(data)
      } else {
        // 如果没有index.json，使用模拟数据
        setArchives([])
      }
    } catch {
      // 错误时使用空数组
      setArchives([])
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return <Loading />
  }

  if (archives.length === 0) {
    return (
      <div className="text-center py-20">
        <div className="text-6xl mb-4">📚</div>
        <h2 className="text-2xl font-semibold text-white mb-2">暂无归档</h2>
        <p className="text-slate-400">
          归档内容将在每日更新后显示
        </p>
      </div>
    )
  }

  return (
    <div>
      <h2 className="text-2xl font-bold text-white mb-6">历史归档</h2>
      <div className="grid gap-4">
        {archives.map((item) => (
          <ArticleCard
            key={item.date}
            date={item.date}
            title={item.title}
            preview={item.preview}
            articleCount={item.articleCount}
          />
        ))}
      </div>
    </div>
  )
}
