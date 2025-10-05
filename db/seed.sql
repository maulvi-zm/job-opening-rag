-- ============================================
-- Sample Data for Testing
-- ============================================

-- Insert sample jobs
INSERT INTO jobs (
    job_title, 
    company_name, 
    location, 
    job_description, 
    requirements,
    gender_preference,
    minimum_age,
    maximum_age,
    minimum_experience_months,
    salary_range,
    job_type,
    education_level,
    skills_required,
    openings_count
) VALUES 
(
    'Software Engineer',
    'Tech Solutions Inc',
    'Jakarta',
    'We are looking for a talented Software Engineer to join our team. You will be responsible for developing and maintaining web applications.',
    'Bachelor degree in Computer Science or related field. Strong knowledge of JavaScript, Node.js, and React. Experience with PostgreSQL and REST APIs.',
    'any',
    22,
    35,
    12,
    'Rp 8.000.000 - Rp 15.000.000',
    'full-time',
    'Bachelor Degree',
    ARRAY['JavaScript', 'Node.js', 'React', 'PostgreSQL', 'REST API'],
    3
),
(
    'Data Analyst',
    'Data Insights Corp',
    'Bandung',
    'Join our data team to analyze business data and provide actionable insights. Work with modern data tools and technologies.',
    'Minimum 1 year experience in data analysis. Proficient in SQL, Python, and data visualization tools. Strong analytical skills.',
    'any',
    21,
    40,
    6,
    'Rp 6.000.000 - Rp 10.000.000',
    'full-time',
    'Bachelor Degree',
    ARRAY['SQL', 'Python', 'Data Analysis', 'Excel', 'Tableau'],
    2
),
(
    'Customer Service Representative',
    'Global Services Ltd',
    'Surabaya',
    'Handle customer inquiries and provide excellent service. Training will be provided.',
    'High school diploma or equivalent. Good communication skills in Indonesian and English. Friendly and patient personality.',
    'any',
    18,
    30,
    0,
    'Rp 4.500.000 - Rp 6.000.000',
    'full-time',
    'High School',
    ARRAY['Communication', 'Customer Service', 'English', 'Problem Solving'],
    5
),
(
    'Marketing Manager',
    'Creative Agency',
    'Jakarta',
    'Lead our marketing team to develop and execute marketing strategies. Drive brand awareness and customer engagement.',
    'Minimum 3 years experience in marketing management. Bachelor degree in Marketing or Business. Proven track record in digital marketing.',
    'any',
    25,
    45,
    36,
    'Rp 12.000.000 - Rp 20.000.000',
    'full-time',
    'Bachelor Degree',
    ARRAY['Marketing Strategy', 'Digital Marketing', 'Team Leadership', 'SEO', 'Social Media'],
    1
),
(
    'Warehouse Staff',
    'Logistics Pro',
    'Tangerang',
    'Handle warehouse operations including receiving, storing, and shipping goods. Physical work required.',
    'Minimum junior high school education. Physically fit and able to lift heavy items. No experience required, training provided.',
    'male',
    18,
    40,
    0,
    'Rp 4.000.000 - Rp 5.500.000',
    'full-time',
    'Junior High School',
    ARRAY['Physical Fitness', 'Warehouse Operations', 'Attention to Detail'],
    10
);

-- Note: Sample user sessions and conversations would be created dynamically by the application

-- INSERT INTO user_sessions (phone_number, current_state, conversation_context, expires_at) VALUES
-- ('+6281234567890', 'searching', '{"filters": {"location": "Jakarta"}, "step": 2}', NOW() + INTERVAL '30 minutes');

-- INSERT INTO conversations (phone_number, session_id, message_text, message_type, intent) VALUES
-- ('+6281234567890', (SELECT session_id FROM user_sessions WHERE phone_number = '+6281234567890' LIMIT 1), 'Hi, I am looking for a job', 'user', 'greeting'),
-- ('+6281234567890', (SELECT session_id FROM user_sessions WHERE phone_number = '+6281234567890' LIMIT 1), 'Hello! I can help you find job openings. What kind of job are you looking for?', 'bot', NULL);

