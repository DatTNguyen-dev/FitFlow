// src/App.jsx
import React, { useState, useEffect } from 'react';
import { 
  Button, Layout, Typography, Card, Row, Col, Progress, Statistic, 
  Menu, Form, Select, Upload, message, Timeline, Tag, List, Avatar, 
  Skeleton, Tooltip, Rate, Divider, Badge
} from 'antd';
import { 
  FireOutlined, ThunderboltOutlined, InboxOutlined, 
  BarChartOutlined, CalendarOutlined, CheckCircleOutlined,
  SmileOutlined, UserOutlined, LineChartOutlined,
  SafetyCertificateOutlined, TrophyOutlined, RocketOutlined
} from '@ant-design/icons';

// Thư viện biểu đồ (Recharts)
import { 
  Radar, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, 
  ResponsiveContainer, BarChart, Bar, XAxis, YAxis, Tooltip as RechartsTooltip 
} from 'recharts';
import { exercisePlanAPI, workoutScheduleAPI, progressReportAPI } from './api/endpoints';

const { Header, Content, Footer } = Layout;
const { Title, Text, Paragraph } = Typography;
const { Dragger } = Upload;
const { Option } = Select;

// --- DỮ LIỆU MOCK (DUMMY DATA - CHỜ BACKEND THAY THẾ) ---
const mockScheduleData = [
  { day: 'Thứ 2', title: 'Ngực & Tay sau', color: 'red', desc: 'Focus: Cơ ngực trên', exercises: ['Bench Press 4x10', 'Push-up 3x15'] },
  { day: 'Thứ 3', title: 'Lưng xô & Tay trước', color: 'blue', desc: 'Focus: Độ rộng lưng', exercises: ['Pull-up 3xMax', 'Lat Pulldown 4x12'] },
  { day: 'Thứ 4', title: 'Cardio & Bụng', color: 'green', desc: 'Đốt mỡ thừa', exercises: ['Chạy bộ 30p', 'Plank 3x1p'] },
  { day: 'Thứ 5', title: 'Chân & Mông', color: 'orange', desc: 'Ngày kinh hoàng', exercises: ['Squat 5x5', 'Leg Press 3x12'] },
  { day: 'Thứ 6', title: 'Vai & Cổ', color: 'purple', desc: 'Vai rộng mặc đồ đẹp', exercises: ['Overhead Press 4x10', 'Face pull 3x15'] },
  { day: 'Thứ 7', title: 'Active Rest', color: 'cyan', desc: 'Giãn cơ nhẹ nhàng', exercises: ['Yoga 45p'] },
];

const mockPerformanceData = [
  { subject: 'Sức mạnh', A: 120, fullMark: 150 },
  { subject: 'Sức bền', A: 98, fullMark: 150 },
  { subject: 'Dẻo dai', A: 86, fullMark: 150 },
  { subject: 'Kỷ luật', A: 99, fullMark: 150 },
  { subject: 'Kỹ thuật', A: 85, fullMark: 150 },
  { subject: 'Dinh dưỡng', A: 65, fullMark: 150 },
];

const mockWeeklyBurn = [
  { name: 'T2', kcal: 400 }, { name: 'T3', kcal: 300 },
  { name: 'T4', kcal: 550 }, { name: 'T5', kcal: 450 },
  { name: 'T6', kcal: 600 }, { name: 'T7', kcal: 200 },
  { name: 'CN', kcal: 100 },
];

// --- CÁC COMPONENT CON (MÀN HÌNH) ---

// 1. DASHBOARD VIEW
const DashboardView = ({ dataTapLuyen, onNavigateCreate }) => (
  <div style={{ animation: 'fadeIn 0.5s' }}>
    <div style={{ textAlign: 'center', marginBottom: 30 }}>
      <Title level={2} style={{ color: '#001529' }}>DASHBOARD TỔNG QUAN</Title>
      <Text type="secondary">"Không có đường tắt nào dẫn đến thành công đâu!"</Text>
    </div>

    <Row gutter={[24, 24]}>
      <Col xs={24} md={8}>
        <Card title="Tiến độ tuần" bordered={false} hoverable>
           <div style={{ textAlign: 'center' }}>
             <Progress type="dashboard" percent={75} strokeColor="#52c41a" />
             <div style={{ marginTop: 10 }}>Đã tập: 4/6 buổi</div>
           </div>
        </Card>
      </Col>
      <Col xs={24} md={8}>
        <Card bordered={false} hoverable style={{ background: '#fff1f0', height: '100%' }}>
          <Statistic title="Calories Đốt Hôm Nay" value={dataTapLuyen.calories} prefix={<FireOutlined style={{color: 'red'}} />} suffix="kcal" />
          <Progress percent={dataTapLuyen.percent} showInfo={false} status="active" strokeColor="red" size="small" style={{ marginTop: 20 }} />
          <Text type="secondary" style={{ fontSize: 12 }}>Mục tiêu: 2000 kcal</Text>
        </Card>
      </Col>
      <Col xs={24} md={8}>
        <Card bordered={false} hoverable style={{ background: '#e6f7ff', height: '100%' }}>
           <Statistic title="Chuỗi ngày tập (Streak)" value={12} prefix={<ThunderboltOutlined style={{color: '#1890ff'}} />} suffix="ngày" />
           <div style={{ marginTop: 15 }}>
             <Tag color="gold">🔥 Kỷ luật thép</Tag>
             <Tag color="blue">💧 Uống đủ nước</Tag>
           </div>
        </Card>
      </Col>
    </Row>
    
    <div style={{ textAlign: 'center', marginTop: 40 }}>
      <Button type="primary" size="large" icon={<ThunderboltOutlined />} onClick={onNavigateCreate}
        style={{ height: 50, borderRadius: 25, padding: '0 40px', background: '#faad14', borderColor: '#faad14' }}>
        THIẾT LẬP MỤC TIÊU MỚI
      </Button>
    </div>
  </div>
);

// 2. CREATE SCHEDULE VIEW (FORM TẠO LỊCH)
const CreateScheduleView = ({ onFinish, isAIProcessing }) => (
  <div style={{ animation: 'fadeIn 0.5s', maxWidth: 600, margin: '0 auto' }}>
     <div style={{ textAlign: 'center', marginBottom: 30 }}>
      <Title level={2}>THIẾT KẾ LỘ TRÌNH</Title>
      <Text>Cung cấp thông tin để AI xây dựng giáo án cho bạn</Text>
    </div>

    <Form layout="vertical" onFinish={onFinish} size="large">
      <Form.Item label="Môn thể thao chính" name="sports" rules={[{ required: true, message: 'Vui lòng chọn môn!' }]}>
        <Select mode="multiple" placeholder="VD: Gym, Yoga...">
          <Option value="gym">🏋️ Gym</Option>
          <Option value="yoga">🧘 Yoga</Option>
          <Option value="boxing">🥊 Boxing</Option>
        </Select>
      </Form.Item>
      
      <Form.Item label="Mục tiêu (Tag)" name="goal" rules={[{ required: true, message: 'Nhập mục tiêu!' }]}>
        <Select mode="tags" placeholder="VD: Giảm 5kg..." tokenSeparators={[',']}>
          <Option value="loss">Giảm cân</Option>
        </Select>
      </Form.Item>

      <Form.Item label="Dữ liệu sức khỏe hiện tại (Upload file)">
        {/* [BACKEND TODO]: Thay action bằng API upload thật */}
        <Dragger style={{ background: '#fff' }}>
          <p className="ant-upload-drag-icon"><InboxOutlined /></p>
          <p className="ant-upload-text">Kéo thả file InBody hoặc lịch cũ</p>
        </Dragger>
      </Form.Item>

      <Button type="primary" htmlType="submit" block size="large" loading={isAIProcessing} 
        style={{ height: 50, marginTop: 20, background: '#001529' }}>
        {isAIProcessing ? 'AI ĐANG SUY NGHĨ...' : 'XÂY DỰNG LỊCH TRÌNH'}
      </Button>
    </Form>
  </div>
);

// 3. SCHEDULE RESULT VIEW (HIỂN THỊ KẾT QUẢ LỊCH)
const ScheduleResultView = () => (
  <div style={{ animation: 'slideRight 0.5s' }}>
    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 20 }}>
      <Title level={3} style={{ margin: 0 }}><CalendarOutlined /> Lịch Tập Tuần Này</Title>
      <Button icon={<RocketOutlined />}>Xuất PDF</Button>
    </div>

    <Row gutter={24}>
      <Col xs={24} md={16}>
        <Card bordered={false} style={{ background: '#fff' }}>
          <Timeline mode="left">
            {mockScheduleData.map((item, index) => (
              <Timeline.Item key={index} color={item.color} label={<Text strong>{item.day}</Text>}>
                <Card size="small" title={item.title} extra={<Tag color={item.color}>Ưu tiên</Tag>} 
                  style={{ boxShadow: '0 2px 5px rgba(0,0,0,0.05)' }}>
                  <Text type="secondary">{item.desc}</Text>
                  <Divider style={{ margin: '10px 0' }} />
                  <List
                    size="small"
                    dataSource={item.exercises}
                    renderItem={ex => <List.Item><CheckCircleOutlined style={{ marginRight: 8, color: '#52c41a' }} /> {ex}</List.Item>}
                  />
                </Card>
              </Timeline.Item>
            ))}
          </Timeline>
        </Card>
      </Col>
      <Col xs={24} md={8}>
        <Card title="Ghi chú HLV AI" style={{ background: '#f6ffed' }}>
          <Paragraph>
            <ul>
              <li>Nhớ khởi động kỹ khớp vai trước khi tập ngực.</li>
              <li>Thứ 5 tập chân nên ăn nhiều Carb hơn.</li>
              <li>Ngủ đủ 8 tiếng để cơ bắp phục hồi.</li>
            </ul>
          </Paragraph>
          <Button type="dashed" block>Hỏi thêm AI</Button>
        </Card>
      </Col>
    </Row>
  </div>
);

// 4. ANALYTICS VIEW (ĐÁNH GIÁ - BIỂU ĐỒ)
const AnalyticsView = () => (
  <div style={{ animation: 'zoomIn 0.5s' }}>
    <div style={{ textAlign: 'center', marginBottom: 30 }}>
      <Title level={2}>BÁO CÁO HIỆU SUẤT</Title>
      <Text type="secondary">Phân tích chỉ số cơ thể & hiệu quả tập luyện</Text>
    </div>

    <Row gutter={[24, 24]}>
      {/* Biểu đồ Radar */}
      <Col xs={24} md={12}>
        <Card title="Biểu đồ Kỹ năng" bordered={false}>
          {/* QUAN TRỌNG: Div bọc ngoài set height để tránh lỗi trắng màn hình */}
          <div style={{ width: '100%', height: 300 }}>
            <ResponsiveContainer width="100%" height="100%">
              <RadarChart cx="50%" cy="50%" outerRadius="80%" data={mockPerformanceData}>
                <PolarGrid />
                <PolarAngleAxis dataKey="subject" />
                <PolarRadiusAxis angle={30} domain={[0, 150]} />
                <Radar name="My Stats" dataKey="A" stroke="#1890ff" fill="#1890ff" fillOpacity={0.6} />
                <RechartsTooltip />
              </RadarChart>
            </ResponsiveContainer>
          </div>
        </Card>
      </Col>

      {/* Biểu đồ Cột */}
      <Col xs={24} md={12}>
        <Card title="Lượng Calo tiêu thụ tuần qua" bordered={false}>
          <div style={{ width: '100%', height: 300 }}>
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={mockWeeklyBurn}>
                <XAxis dataKey="name" />
                <YAxis />
                <RechartsTooltip />
                <Bar dataKey="kcal" fill="#ff7a45" barSize={30} radius={[5, 5, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </Card>
      </Col>
    </Row>

    <Row gutter={[24, 24]} style={{ marginTop: 24 }}>
      <Col xs={24} md={24}>
        <Card title={<><SafetyCertificateOutlined /> Đánh giá chi tiết từ AI</>} bordered={false}>
          <List itemLayout="horizontal">
            <List.Item>
              <List.Item.Meta
                avatar={<Avatar style={{ backgroundColor: '#fde3cf', color: '#f56a00' }}>A</Avatar>}
                title="Sự kiên trì"
                description="Bạn đã duy trì lịch tập rất tốt, không bỏ buổi nào trong 2 tuần qua."
              />
              <Rate disabled defaultValue={5} />
            </List.Item>
            <List.Item>
              <List.Item.Meta
                avatar={<Avatar style={{ backgroundColor: '#87d068' }} icon={<UserOutlined />} />}
                title="Cường độ tập luyện"
                description="Cường độ trung bình. Đề xuất tăng tạ thêm 5% vào tuần sau."
              />
              <Rate disabled defaultValue={4} />
            </List.Item>
          </List>
        </Card>
      </Col>
    </Row>
  </div>
);

// --- MAIN APP ---
function App() {
  const [currentTab, setCurrentTab] = useState('dashboard');
  const [isAIProcessing, setIsAIProcessing] = useState(false);
  const [dataTapLuyen, setDataTapLuyen] = useState({ calories: 1200, percent: 60 });
  
  useEffect(() => {
    const timer = setInterval(() => {
      setDataTapLuyen(prev => ({
        calories: prev.calories + Math.floor(Math.random() * 5),
        percent: prev.percent < 100 ? prev.percent + 0.1 : 100
      }));
    }, 3000);
    return () => clearInterval(timer);
  }, []);

  const handleBuildSchedule = async (values) => {
    console.log("Dữ liệu gửi đi:", values);
    setIsAIProcessing(true);
    try {
      const response = await exercisePlanAPI.generatePlan({
        sports: values.sports,
        goal: values.goal,
        level: values.level,
      });
      
      console.log("Response từ backend:", response.data);
      
      // Generate schedule sau khi có plan
      const scheduleResponse = await workoutScheduleAPI.generateSchedule({
        preferred_times: values.preferred_times,
      });
      
      message.success('Đã tạo xong lịch trình!');
      setCurrentTab('schedule');
    } catch (error) {
      message.error('Lỗi tạo lịch trình: ' + error.message);
      console.error(error);
    } finally {
      setIsAIProcessing(false);
    }
  };

  const menuItems = [
    { key: 'dashboard', icon: <BarChartOutlined />, label: 'Dashboard' },
    { key: 'create', icon: <ThunderboltOutlined />, label: 'Tạo Lịch' },
    { key: 'schedule', icon: <CalendarOutlined />, label: 'Lịch Trình' },
    { key: 'review', icon: <LineChartOutlined />, label: 'Đánh Giá' },
  ];

  return (
    <Layout style={{ minHeight: '100vh', backgroundImage: "url('https://images.unsplash.com/photo-1534438327276-14e5300c3a48?q=80&w=1470&auto=format&fit=crop')", backgroundSize: 'cover', backgroundAttachment: 'fixed' }}>
      <div style={{ position: 'absolute', top: 0, left: 0, right: 0, bottom: 0, background: 'rgba(0,0,0,0.7)', zIndex: 0 }} />
      
      {/* HEADER */}
      <Header style={{ position: 'sticky', top: 0, zIndex: 100, display: 'flex', alignItems: 'center', justifyContent: 'space-between', background: 'rgba(0, 21, 41, 0.9)', padding: '0 20px', borderBottom: '1px solid rgba(255,255,255,0.1)' }}>
        <div style={{ display: 'flex', alignItems: 'center' }}>
          <h2 style={{ color: '#fff', margin: '0 30px 0 0', fontStyle: 'italic', cursor: 'pointer' }} onClick={() => setCurrentTab('dashboard')}>FITFLOW</h2>
          <Menu 
            theme="dark" mode="horizontal" selectedKeys={[currentTab]} 
            items={menuItems} onClick={(e) => setCurrentTab(e.key)}
            style={{ background: 'transparent', minWidth: 400, borderBottom: 'none' }} 
          />
        </div>
        <div style={{ display: 'flex', gap: 15, alignItems: 'center' }}>
          <Badge count={1} dot><Avatar style={{ backgroundColor: '#87d068' }} icon={<UserOutlined />} /></Badge>
          <span style={{color: 'white'}}>Gymer Pro</span>
        </div>
      </Header>

      {/* CONTENT */}
      <Content style={{ padding: '30px', display: 'flex', justifyContent: 'center', zIndex: 1 }}>
        <div style={{ background: '#fff', padding: 30, borderRadius: 16, maxWidth: 1200, width: '100%', minHeight: 600, boxShadow: '0 10px 30px rgba(0,0,0,0.5)' }}>
          {currentTab === 'dashboard' && <DashboardView dataTapLuyen={dataTapLuyen} onNavigateCreate={() => setCurrentTab('create')} />}
          {currentTab === 'create' && <CreateScheduleView onFinish={handleBuildSchedule} isAIProcessing={isAIProcessing} />}
          {currentTab === 'schedule' && <ScheduleResultView />}
          {currentTab === 'review' && <AnalyticsView />}
        </div>
      </Content>
      
      <Footer style={{ textAlign: 'center', background: 'transparent', color: 'rgba(255,255,255,0.5)', zIndex: 1 }}>FitFlow ©2026</Footer>
    </Layout>
  );
}

export default App;