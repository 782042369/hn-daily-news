import { Link } from 'react-router-dom'
import { format, parseISO } from 'date-fns'
import { zhCN } from 'date-fns/locale'

interface ArticleCardProps {
  date: string
  title: string
  preview?: string
  articleCount?: number
}

export default function ArticleCard({ date, title, preview, articleCount }: ArticleCardProps) {
  const formattedDate = format(parseISO(date), 'yyyy年M月d日 EEEE', { locale: zhCN })
  
  return (
    <Link to={`/${date}`} className="block">
      <div className="bg-slate-800 rounded-lg p-6 hover:bg-slate-750 transition-colors border border-slate-700 hover:border-orange-500/50">
        <div className="flex items-start justify-between">
          <div className="flex-1">
            <h3 className="text-lg font-semibold text-white mb-2">{title}</h3>
            <p className="text-slate-400 text-sm mb-3">{formattedDate}</p>
            {preview && (
              <p className="text-slate-500 text-sm line-clamp-2">{preview}</p>
            )}
          </div>
          {articleCount && (
            <div className="ml-4 px-3 py-1 bg-orange-500/20 text-orange-400 rounded-full text-sm">
              {articleCount} 篇
            </div>
          )}
        </div>
      </div>
    </Link>
  )
}
