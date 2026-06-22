-- 1. 비우기
DELETE FROM npcs;

-- 2. 확인 (선택사항 - sqlite3 CLI에서만 작동)
-- SELECT COUNT(*) FROM npcs;

-- 3. 초기 NPC 10명 삽입
INSERT INTO npcs (npc_id, name, persona, genetic_seed) VALUES
('npc_w01', 'Aria', '{"background": "A wise healer", "info_disclosure": "open"}', '{"appearance": "silver hair, gentle eyes", "personality": "calm and nurturing", "ability": "high wisdom, low strength", "story": "Born under a full moon", "mutation_chance": 0.05}'),
('npc_w02', 'Draven', '{"background": "A ruthless mercenary", "info_disclosure": "hidden"}', '{"appearance": "scarred face, dark eyes", "personality": "cold and calculating", "ability": "high strength, low empathy", "story": "Orphaned by war", "mutation_chance": 0.15}'),
('npc_w03', 'Lyra', '{"background": "A wandering bard", "info_disclosure": "selective"}', '{"appearance": "auburn curls, bright smile", "personality": "charismatic and curious", "ability": "high charisma, average combat", "story": "Travels to collect stories", "mutation_chance": 0.1}'),
('npc_w04', 'Theron', '{"background": "A disgraced knight", "info_disclosure": "selective"}', '{"appearance": "tall, weathered armor", "personality": "honorable but broken", "ability": "high combat, low morale", "story": "Lost his lord in battle", "mutation_chance": 0.08}'),
('npc_w05', 'Sable', '{"background": "A cunning thief", "info_disclosure": "hidden"}', '{"appearance": "slim, dark cloak", "personality": "witty and deceptive", "ability": "high agility, low trust", "story": "Stole to survive", "mutation_chance": 0.2}'),
('npc_w06', 'Orin', '{"background": "A hermit scholar", "info_disclosure": "selective"}', '{"appearance": "frail, ink-stained fingers", "personality": "eccentric and brilliant", "ability": "high intellect, low social", "story": "Seeks forbidden knowledge", "mutation_chance": 0.12}'),
('npc_w07', 'Mira', '{"background": "A merchant princess", "info_disclosure": "open"}', '{"appearance": "elegant, sharp eyes", "personality": "ambitious and charming", "ability": "high negotiation, average combat", "story": "Built wealth from nothing", "mutation_chance": 0.07}'),
('npc_w08', 'Gareth', '{"background": "A retired general", "info_disclosure": "selective"}', '{"appearance": "stocky, grey beard", "personality": "stern but fair", "ability": "high tactics, low patience", "story": "Won a war, lost a son", "mutation_chance": 0.06}'),
('npc_w09', 'Vesper', '{"background": "A mysterious oracle", "info_disclosure": "hidden"}', '{"appearance": "pale, distant gaze", "personality": "cryptic and detached", "ability": "high foresight, low action", "story": "Sees futures she cannot change", "mutation_chance": 0.25}'),
('npc_w10', 'Finn', '{"background": "A young farmhand turned hero", "info_disclosure": "open"}', '{"appearance": "freckled, bright eyes", "personality": "naive but brave", "ability": "high potential, low experience", "story": "Left home to find purpose", "mutation_chance": 0.3}');