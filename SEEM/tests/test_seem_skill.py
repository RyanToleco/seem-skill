"""
SEEM Skill 单元测试
"""

import unittest
import json
from unittest.mock import Mock, patch
import numpy as np

from SEEM import SEEMSkill, SEEMConfig, RetrieveStrategy, EpisodicMemory
from SEEM.core.utils import cosine_similarity, generate_memory_id


class TestSEEMSkill(unittest.TestCase):
    """SEEM Skill 测试类"""
    
    def setUp(self):
        """测试前准备"""
        self.config = SEEMConfig(
            llm_api_key="test-key",
            mm_encoder_api_key="test-key",
            retrieve_strategy=RetrieveStrategy.DPR,
            enable_cache=False,
            enable_integration=False  # 测试时不启用整合
        )
        self.skill = SEEMSkill(self.config)
    
    def test_store_basic(self):
        """测试基本存储功能"""
        observation = {
            "dialogue_id": "D1:1",
            "text": "Lena asked about Scottish Terriers.",
            "timestamp": "2023-01-15T10:00:00"
        }
        
        # Mock LLM 和 Encoder
        with patch.object(self.skill.llm, 'generate') as mock_llm, \
             patch.object(self.skill.mm_encoder, 'encode_text') as mock_encoder:
            
            # Mock LLM 返回
            mock_llm.return_value = json.dumps({
                "summary": "Lena asked about Scottish Terriers.",
                "events": [{"participants": ["Lena"], "action": ["asked about Scottish Terriers"]}]
            })
            
            # Mock Encoder 返回
            mock_encoder.return_value = np.random.rand(768).astype(np.float32)
            
            # 执行存储
            memory_id = self.skill.store(observation)
            
            # 验证
            self.assertIsNotNone(memory_id)
            self.assertIn(memory_id, self.skill.memories)
            self.assertEqual(len(self.skill.memories), 1)
            self.assertEqual(len(self.skill.chunk_store), 1)
    
    def test_recall_basic(self):
        """测试基本检索功能"""
        # 先存储
        self.skill.memories["M1"] = EpisodicMemory(
            memory_id="M1",
            chunk_ids=["D1:1"],
            summary="Test summary",
            events=[]
        )
        self.skill.memory_embeddings["M1"] = np.random.rand(768).astype(np.float32)
        self.skill.chunk_store["D1:1"] = {
            "dialogue_id": "D1:1",
            "text": "Test text"
        }
        
        # Mock Encoder
        with patch.object(self.skill.mm_encoder, 'encode_text') as mock_encoder:
            mock_encoder.return_value = np.random.rand(768).astype(np.float32)
            
            # 执行检索
            query = {"text": "Test query"}
            results = self.skill.recall(query, top_k=1)
            
            # 验证
            self.assertEqual(len(results), 1)
            self.assertIn("text", results[0])
            self.assertIn("dialogue_id", results[0])
    
    def test_reset(self):
        """测试重置功能"""
        # 添加数据
        self.skill.memories["M1"] = EpisodicMemory(
            memory_id="M1",
            chunk_ids=["D1:1"],
            summary="Test",
            events=[]
        )
        
        # 重置
        self.skill.reset()
        
        # 验证
        self.assertEqual(len(self.skill.memories), 0)
        self.assertEqual(len(self.skill.chunk_store), 0)
        self.assertEqual(len(self.skill.memory_embeddings), 0)
    
    def test_cosine_similarity(self):
        """测试余弦相似度计算"""
        vec1 = np.array([1.0, 0.0, 0.0])
        vec2 = np.array([1.0, 0.0, 0.0])
        vec3 = np.array([0.0, 1.0, 0.0])
        
        # 相同向量
        self.assertAlmostEqual(cosine_similarity(vec1, vec2), 1.0, places=5)
        
        # 正交向量
        self.assertAlmostEqual(cosine_similarity(vec1, vec3), 0.0, places=5)
    
    def test_generate_memory_id(self):
        """测试记忆 ID 生成"""
        id1 = generate_memory_id()
        id2 = generate_memory_id()
        
        self.assertNotEqual(id1, id2)
        self.assertEqual(len(id1), 16)  # MD5 前 16 位
    
    def test_display_memories(self):
        """测试记忆展示功能"""
        # 添加测试数据
        self.skill.memories["M1"] = EpisodicMemory(
            memory_id="M1",
            chunk_ids=["D1:1"],
            summary="Lena asked about Scottish Terriers.",
            events=[{"participants": ["Lena"], "action": ["asked about Scottish Terriers"]}],
            image_ids=[]
        )
        self.skill.chunk_store["D1:1"] = {
            "dialogue_id": "D1:1",
            "speaker": "Lena",
            "text": "Lena asked about Scottish Terriers.",
            "timestamp": "2023-01-15T10:00:00"
        }
        
        self.skill.memories["M2"] = EpisodicMemory(
            memory_id="M2",
            chunk_ids=["D1:2"],
            summary="The assistant explained about Scottish Terriers.",
            events=[{"participants": ["Assistant"], "action": ["explained about Scottish Terriers"]}],
            image_ids=[]
        )
        self.skill.chunk_store["D1:2"] = {
            "dialogue_id": "D1:2",
            "speaker": "Assistant",
            "text": "The assistant explained about Scottish Terriers.",
            "timestamp": "2023-01-15T10:01:00"
        }
        
        # 测试展示所有记忆
        output = self.skill.display_memories()
        self.assertIn("SEEM Episodic Memory Display", output)
        self.assertIn("Lena", output)
        self.assertIn("Assistant", output)
        self.assertIn("M1", output)
        self.assertIn("M2", output)
        
        # 测试按 dialogue_id 筛选
        filtered_output = self.skill.display_memories(dialogue_id="D1:1")
        self.assertIn("D1:1", filtered_output)
        self.assertNotIn("D1:2", filtered_output)
        
        # 测试空记忆情况
        empty_skill = SEEMSkill(self.config)
        empty_output = empty_skill.display_memories()
        self.assertEqual(empty_output, "No memories stored yet.")
    
    @unittest.skip("需要实际 API Key")
    def test_integration_with_real_api(self):
        """测试真实 API 调用（需要有效 API Key）"""
        config = SEEMConfig(
            llm_api_key="your-real-api-key",
            mm_encoder_api_key="your-real-api-key"
        )
        skill = SEEMSkill(config)
        
        observation = {
            "dialogue_id": "D1:1",
            "text": "Lena asked about Scottish Terriers."
        }
        
        memory_id = skill.store(observation)
        self.assertIsNotNone(memory_id)
        
        query = {"text": "What did Lena ask?"}
        results = skill.recall(query, top_k=1)
        self.assertEqual(len(results), 1)


class TestEpisodicMemory(unittest.TestCase):
    """测试 EpisodicMemory 数据结构"""
    
    def test_to_dict(self):
        """测试转换为字典"""
        memory = EpisodicMemory(
            memory_id="M1",
            chunk_ids=["D1:1", "D1:2"],
            summary="Test summary",
            events=[{"participants": ["Lena"], "action": ["asked"]}],
            image_ids=["img_001"]
        )
        
        data = memory.to_dict()
        
        self.assertEqual(data["memory_id"], "M1")
        self.assertEqual(data["chunk_ids"], ["D1:1", "D1:2"])
        self.assertEqual(data["summary"], "Test summary")
        self.assertEqual(len(data["events"]), 1)
    
    def test_from_dict(self):
        """测试从字典创建"""
        data = {
            "memory_id": "M1",
            "chunk_ids": ["D1:1"],
            "summary": "Test",
            "events": [],
            "image_ids": []
        }
        
        memory = EpisodicMemory.from_dict(data)
        
        self.assertEqual(memory.memory_id, "M1")
        self.assertEqual(memory.summary, "Test")


if __name__ == "__main__":
    unittest.main()
