
import { FC, ReactNode } from 'react';
import { Card } from "@/components/ui/card";

interface AgentResultCardProps {
  title: string;
  icon?: ReactNode;
  children: ReactNode;
}

const AgentResultCard: FC<AgentResultCardProps> = ({ title, icon, children }) => {
  return (
    <Card className="border border-sbi-gray/20 shadow-md rounded-lg overflow-hidden">
      <div className="bg-gradient-to-r from-sbi-cyan/20 to-white p-4 border-b border-sbi-gray/10">
        <div className="flex items-center space-x-3">
          {icon && <div className="text-sbi-cyan">{icon}</div>}
          <h3 className="text-xl font-semibold text-sbi-blue">{title}</h3>
        </div>
      </div>
      <div className="p-6">
        {children}
      </div>
    </Card>
  );
};

export default AgentResultCard;
