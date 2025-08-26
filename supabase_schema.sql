-- Schema do BI de Perdas (Supabase)
-- Tabelas: filiais e lancamentos

-- Tabela de filiais
CREATE TABLE IF NOT EXISTS public.filiais (
  id BIGSERIAL PRIMARY KEY,
  nome TEXT NOT NULL UNIQUE,
  endereco TEXT,
  cidade TEXT,
  estado TEXT,
  telefone TEXT,
  gerente TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Tabela de lançamentos de perdas
CREATE TABLE IF NOT EXISTS public.lancamentos (
  id BIGSERIAL PRIMARY KEY,
  data DATE NOT NULL,
  setor TEXT NOT NULL,
  filial TEXT NOT NULL,
  "precoPerda" NUMERIC NOT NULL DEFAULT 0,
  "precoVenda" NUMERIC NOT NULL DEFAULT 0,
  observacoes TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Índices para melhor performance
CREATE INDEX IF NOT EXISTS idx_lancamentos_data ON public.lancamentos(data);
CREATE INDEX IF NOT EXISTS idx_lancamentos_setor ON public.lancamentos(setor);
CREATE INDEX IF NOT EXISTS idx_lancamentos_filial ON public.lancamentos(filial);
CREATE INDEX IF NOT EXISTS idx_filiais_nome ON public.filiais(nome);

-- Políticas RLS (Row Level Security) - Desabilitadas para simplicidade inicial
-- Para habilitar segurança mais rígida, descomente as linhas abaixo:

-- ALTER TABLE public.filiais ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE public.lancamentos ENABLE ROW LEVEL SECURITY;

-- CREATE POLICY "anon_select_filiais" ON public.filiais FOR SELECT USING (true);
-- CREATE POLICY "anon_insert_filiais" ON public.filiais FOR INSERT WITH CHECK (true);
-- CREATE POLICY "anon_update_filiais" ON public.filiais FOR UPDATE USING (true);
-- CREATE POLICY "anon_delete_filiais" ON public.filiais FOR DELETE USING (true);

-- CREATE POLICY "anon_select_lancamentos" ON public.lancamentos FOR SELECT USING (true);
-- CREATE POLICY "anon_insert_lancamentos" ON public.lancamentos FOR INSERT WITH CHECK (true);
-- CREATE POLICY "anon_update_lancamentos" ON public.lancamentos FOR UPDATE USING (true);
-- CREATE POLICY "anon_delete_lancamentos" ON public.lancamentos FOR DELETE USING (true);

-- Dados de exemplo (opcional)
INSERT INTO public.filiais (nome, endereco, cidade, estado, telefone, gerente) VALUES
('Filial Centro', 'Rua das Flores, 123', 'São Paulo', 'SP', '(11) 1234-5678', 'João Silva'),
('Filial Norte', 'Av. Paulista, 456', 'São Paulo', 'SP', '(11) 2345-6789', 'Maria Santos'),
('Filial Sul', 'Rua Augusta, 789', 'São Paulo', 'SP', '(11) 3456-7890', 'Pedro Costa')
ON CONFLICT (nome) DO NOTHING;

-- Exemplo de lançamentos
INSERT INTO public.lancamentos (data, setor, filial, "precoPerda", "precoVenda", observacoes) VALUES
('2024-01-15', 'Açougue', 'Filial Centro', 150.50, 3000.00, 'Carne vencida'),
('2024-01-15', 'Hortifruti', 'Filial Centro', 89.30, 1500.00, 'Frutas estragadas'),
('2024-01-16', 'Padaria', 'Filial Norte', 45.20, 800.00, 'Pães do dia anterior'),
('2024-01-16', 'Frios', 'Filial Sul', 120.75, 2200.00, 'Produtos próximos ao vencimento')
ON CONFLICT DO NOTHING;

