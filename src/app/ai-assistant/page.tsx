import React from 'react';
import { Card } from '@/components/ui/Card';
import { Bot, Send, ShieldAlert } from 'lucide-react';
import { Badge } from '@/components/ui/Badge';
import styles from '../page.module.css';
import widgetStyles from '@/components/dashboard/BottomWidgets.module.css';

export default function AIAssistantPage() {
  return (
    <div className={styles.dashboard}>
      <Card title="AI Assistant" action={<Badge variant="blue">Beta</Badge>}>
        <div style={{ padding: '24px', display: 'flex', flexDirection: 'column', height: '600px' }}>
          <div className={widgetStyles.chatBox}>
            <div className={widgetStyles.aiWelcome}>
              <ShieldAlert size={16} />
              <span>Ask me anything about the city, traffic, flood risk, hospitals or emergency routes...</span>
            </div>
            
            <div className={widgetStyles.promptBtn}>Which route should an ambulance take from Bandra to Lilavati Hospital?</div>
            <div className={widgetStyles.promptBtn}>What happens if rainfall increases by 50%?</div>
            <div className={widgetStyles.promptBtn}>Show nearest hospital to my location</div>
          </div>
          
          <div className={widgetStyles.chatInputBox} style={{ marginTop: 'auto' }}>
            <input type="text" placeholder="Type your question..." className={widgetStyles.chatInput} />
            <button className={widgetStyles.sendBtn}><Send size={16} /></button>
          </div>
        </div>
      </Card>
    </div>
  );
}
