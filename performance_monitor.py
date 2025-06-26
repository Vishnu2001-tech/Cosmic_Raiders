"""
Performance Monitor for Cosmic Raiders
Tracks FPS, memory usage, and performance metrics
"""

import pygame
import time
import psutil
import os

class PerformanceMonitor:
    def __init__(self, target_fps=60):
        self.target_fps = target_fps
        self.frame_times = []
        self.max_frame_history = 60  # Track last 60 frames
        self.last_time = time.time()
        self.frame_count = 0
        self.fps = 0
        self.avg_fps = 0
        self.min_fps = float('inf')
        self.max_fps = 0
        
        # Performance tracking
        self.process = psutil.Process(os.getpid())
        self.memory_usage = 0
        self.cpu_usage = 0
        
        # Performance warnings
        self.low_fps_threshold = target_fps * 0.8  # 80% of target
        self.high_memory_threshold = 100 * 1024 * 1024  # 100MB
        
        self.warnings = []
        
    def update(self):
        """Update performance metrics"""
        current_time = time.time()
        frame_time = current_time - self.last_time
        self.last_time = current_time
        
        # Track frame times
        self.frame_times.append(frame_time)
        if len(self.frame_times) > self.max_frame_history:
            self.frame_times.pop(0)
        
        # Calculate FPS
        if frame_time > 0:
            self.fps = 1.0 / frame_time
            self.min_fps = min(self.min_fps, self.fps)
            self.max_fps = max(self.max_fps, self.fps)
        
        # Calculate average FPS
        if self.frame_times:
            avg_frame_time = sum(self.frame_times) / len(self.frame_times)
            self.avg_fps = 1.0 / avg_frame_time if avg_frame_time > 0 else 0
        
        self.frame_count += 1
        
        # Update system metrics every 30 frames
        if self.frame_count % 30 == 0:
            try:
                self.memory_usage = self.process.memory_info().rss
                self.cpu_usage = self.process.cpu_percent()
                self._check_performance_warnings()
            except:
                pass  # Ignore errors in performance monitoring
    
    def _check_performance_warnings(self):
        """Check for performance issues"""
        # Clear old warnings
        self.warnings.clear()
        
        # Check FPS
        if self.avg_fps < self.low_fps_threshold:
            self.warnings.append(f"Low FPS: {self.avg_fps:.1f} (target: {self.target_fps})")
        
        # Check memory usage
        if self.memory_usage > self.high_memory_threshold:
            memory_mb = self.memory_usage / (1024 * 1024)
            self.warnings.append(f"High memory usage: {memory_mb:.1f}MB")
        
        # Check CPU usage
        if self.cpu_usage > 80:
            self.warnings.append(f"High CPU usage: {self.cpu_usage:.1f}%")
    
    def get_stats(self):
        """Get performance statistics"""
        memory_mb = self.memory_usage / (1024 * 1024)
        return {
            'fps': self.fps,
            'avg_fps': self.avg_fps,
            'min_fps': self.min_fps,
            'max_fps': self.max_fps,
            'memory_mb': memory_mb,
            'cpu_percent': self.cpu_usage,
            'frame_count': self.frame_count,
            'warnings': self.warnings.copy()
        }
    
    def draw_debug_info(self, screen, font, x=10, y=10):
        """Draw performance info on screen (for debugging)"""
        if not font:
            return
        
        stats = self.get_stats()
        debug_lines = [
            f"FPS: {stats['fps']:.1f} (avg: {stats['avg_fps']:.1f})",
            f"Memory: {stats['memory_mb']:.1f}MB",
            f"CPU: {stats['cpu_percent']:.1f}%",
            f"Frames: {stats['frame_count']}"
        ]
        
        # Add warnings
        for warning in stats['warnings']:
            debug_lines.append(f"⚠️ {warning}")
        
        # Draw debug info
        for i, line in enumerate(debug_lines):
            color = (255, 255, 0) if line.startswith('⚠️') else (255, 255, 255)
            try:
                text_surface = font.render(line, True, color)
                screen.blit(text_surface, (x, y + i * 20))
            except:
                pass  # Ignore font rendering errors
    
    def reset_stats(self):
        """Reset performance statistics"""
        self.frame_times.clear()
        self.frame_count = 0
        self.min_fps = float('inf')
        self.max_fps = 0
        self.warnings.clear()
    
    def is_performance_good(self):
        """Check if performance is acceptable"""
        return (self.avg_fps >= self.low_fps_threshold and 
                self.memory_usage < self.high_memory_threshold and
                self.cpu_usage < 80)
