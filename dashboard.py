import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime, timedelta
import database as db
import altair as alt

class Dashboard:
    def __init__(self):
        self.colors = {
            'primary': '#4B8BBE',
            'secondary': '#FF4B4B',
            'background': '#f0f4f8',
            'text': '#333333'
        }

    def show_learning_progress(self, user_id):
        """Display learning progress charts"""
        progress = db.get_user_progress(user_id)
        if not progress:
            st.info("No learning progress data available yet.")
            return

        # Convert to DataFrame
        df = pd.DataFrame(progress)
        
        # Topic mastery chart
        fig = px.bar(
            df,
            x='topic',
            y='avg_score',
            title='Topic Mastery',
            labels={'avg_score': 'Average Score (%)', 'topic': 'Topic'},
            color='avg_score',
            color_continuous_scale=['#FF4B4B', '#4B8BBE']
        )
        fig.update_layout(
            plot_bgcolor=self.colors['background'],
            paper_bgcolor=self.colors['background'],
            font={'color': self.colors['text']}
        )
        st.plotly_chart(fig, use_container_width=True)

        # Study time distribution
        fig = px.pie(
            df,
            values='total_time',
            names='topic',
            title='Study Time Distribution',
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        fig.update_layout(
            plot_bgcolor=self.colors['background'],
            paper_bgcolor=self.colors['background'],
            font={'color': self.colors['text']}
        )
        st.plotly_chart(fig, use_container_width=True)

    def show_quiz_performance(self, user_id):
        """Display quiz performance metrics"""
        quiz_history = db.get_quiz_history(user_id)
        if not quiz_history:
            st.info("No quiz history available yet.")
            return

        # Convert to DataFrame
        df = pd.DataFrame(quiz_history)
        df['completed_at'] = pd.to_datetime(df['completed_at'])
        
        # Quiz scores over time
        fig = px.line(
            df,
            x='completed_at',
            y='score',
            title='Quiz Performance Over Time',
            labels={'score': 'Score (%)', 'completed_at': 'Date'},
            markers=True
        )
        fig.update_layout(
            plot_bgcolor=self.colors['background'],
            paper_bgcolor=self.colors['background'],
            font={'color': self.colors['text']}
        )
        st.plotly_chart(fig, use_container_width=True)

        # Quiz topic performance
        topic_stats = df.groupby('quiz_topic').agg({
            'score': ['mean', 'count']
        }).reset_index()
        topic_stats.columns = ['topic', 'avg_score', 'attempts']
        
        fig = px.scatter(
            topic_stats,
            x='attempts',
            y='avg_score',
            size='attempts',
            color='avg_score',
            hover_name='topic',
            title='Topic Performance Overview',
            labels={
                'avg_score': 'Average Score (%)',
                'attempts': 'Number of Attempts'
            }
        )
        fig.update_layout(
            plot_bgcolor=self.colors['background'],
            paper_bgcolor=self.colors['background'],
            font={'color': self.colors['text']}
        )
        st.plotly_chart(fig, use_container_width=True)

    def show_study_analytics(self, user_id):
        """Display study analytics"""
        stats = db.get_study_stats(user_id)
        if not stats:
            st.info("No study statistics available yet.")
            return

        # Create metrics cards
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                "Topics Studied",
                stats['topics_studied'],
                delta=None
            )
        
        with col2:
            total_time = stats['total_time'] if stats['total_time'] is not None else 0
            hours_studied = round(total_time / 3600, 1)
            st.metric(
                "Hours Studied",
                hours_studied,
                delta=None
            )
        
        with col3:
            st.metric(
                "Study Days",
                stats['days_studied'],
                delta=None
            )

        # Study streak calendar
        study_sessions = db.get_study_sessions(user_id)
        if study_sessions:
            df = pd.DataFrame(study_sessions)
            df['date'] = pd.to_datetime(df['start_time']).dt.date
            
            # Create calendar heatmap
            calendar_data = df.groupby('date').size().reset_index(name='count')
            calendar_data['date'] = pd.to_datetime(calendar_data['date'])
            
            fig = px.density_heatmap(
                calendar_data,
                x=calendar_data['date'].dt.day_name(),
                y=calendar_data['date'].dt.isocalendar().week,
                z='count',
                title='Study Activity Calendar',
                color_continuous_scale=['#f0f4f8', '#4B8BBE']
            )
            fig.update_layout(
                plot_bgcolor=self.colors['background'],
                paper_bgcolor=self.colors['background'],
                font={'color': self.colors['text']}
            )
            st.plotly_chart(fig, use_container_width=True)

    def show_achievements(self, user_id):
        """Display user achievements"""
        achievements = db.get_user_achievements(user_id)
        if not achievements:
            st.info("No achievements earned yet.")
            return

        # Create achievement cards
        cols = st.columns(3)
        for idx, achievement in enumerate(achievements):
            with cols[idx % 3]:
                st.markdown(f"""
                    <div style="
                        background-color: white;
                        padding: 20px;
                        border-radius: 10px;
                        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                        text-align: center;
                    ">
                        <h3 style="color: {self.colors['primary']};">🏆 {achievement['achievement_type']}</h3>
                        <p style="color: {self.colors['text']};">Earned on {achievement['earned_at']}</p>
                    </div>
                """, unsafe_allow_html=True)

    def show_learning_path(self, user_id):
        """Display recommended learning path"""
        progress = db.get_user_progress(user_id)
        if not progress:
            st.info("Complete some lessons to get personalized recommendations.")
            return

        # Create learning path visualization
        topics = [p['topic'] for p in progress]
        scores = [p['avg_score'] for p in progress]
        
        fig = go.Figure()
        
        # Add nodes
        fig.add_trace(go.Scatter(
            x=[i for i in range(len(topics))],
            y=scores,
            mode='markers+lines+text',
            marker=dict(
                size=20,
                color=scores,
                colorscale='Viridis',
                showscale=True
            ),
            text=topics,
            textposition="top center"
        ))
        
        fig.update_layout(
            title='Learning Path Progress',
            xaxis_title='Learning Sequence',
            yaxis_title='Mastery Level (%)',
            plot_bgcolor=self.colors['background'],
            paper_bgcolor=self.colors['background'],
            font={'color': self.colors['text']}
        )
        
        st.plotly_chart(fig, use_container_width=True)

# Initialize dashboard
dashboard = Dashboard() 