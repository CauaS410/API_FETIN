import { useState } from 'react';
import { Link } from 'react-router-dom';
import './nomeCadastro.css';

function Register() {
  const [nome, setNome] = useState('');
  const [email, setEmail] = useState('');
  const [celular, setCelular] = useState('');
  const [deviceId, setDeviceId] = useState('');
  const [senha, setSenha] = useState('');
  const [mensagem, setMensagem] = useState({ texto: '', tipo: '' });

  const handleSubmit = async (event) => {
    event.preventDefault();

    setMensagem({
      texto: 'Criando conta...',
      tipo: 'info',
    });

    try {
      const resposta = await fetch('http://localhost:8000/users/create', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          name: nome,
          email: email,
          cell: celular,
          deviceId: deviceId,
          password: senha,
        }),
      });

      const dados = await resposta.json();

      if (resposta.status === 200) {
        setMensagem({
          texto: 'Cadastro realizado com sucesso!',
          tipo: 'sucesso',
        });

        setNome('');
        setEmail('');
        setCelular('');
        setDeviceId('');
        setSenha('');
      } else if (resposta.status === 400) {
        setMensagem({
          texto: dados.detail,
          tipo: 'erro',
        });
      } else if (resposta.status === 422) {
        const primeiroErro =
          dados.detail?.[0]?.msg || 'Dados inválidos.';

        setMensagem({
          texto: primeiroErro,
          tipo: 'erro',
        });
      } else {
        setMensagem({
          texto: 'Erro ao realizar cadastro.',
          tipo: 'erro',
        });
      }
    } catch (erro) {
      setMensagem({
        texto: 'Erro de conexão com o servidor.',
        tipo: 'erro',
      });

      console.error(erro);
    }
  };

  return (
    <div className="page-center">
      <div className="cadastro-container">

        <h2>Criar conta</h2>

        <p className="subtitulo">
          Preencha os dados para começar.
        </p>

        <form onSubmit={handleSubmit}>

          <div className="form-group">
            <label htmlFor="nome">Nome completo</label>
            <input
              type="text"
              id="nome"
              placeholder="Digite seu nome"
              required
              value={nome}
              onChange={(e) => setNome(e.target.value)}
            />
          </div>

          <div className="form-group">
            <label htmlFor="email">E-mail</label>
            <input
              type="email"
              id="email"
              placeholder="Digite seu e-mail"
              required
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />
          </div>

          <div className="form-group">
            <label htmlFor="celular">Celular</label>
            <input
              type="text"
              id="celular"
              placeholder="(00) 00000-0000"
              required
              value={celular}
              onChange={(e) => setCelular(e.target.value)}
            />
          </div>

          <div className="form-group">
            <label htmlFor="deviceId">Identificador do sensor</label>
            <input
              type="text"
              id="deviceId"
              placeholder="Ex: esp32-01"
              required
              value={deviceId}
              onChange={(e) => setDeviceId(e.target.value)}
            />
          </div>

          <div className="form-group">
            <label htmlFor="senha">Senha</label>
            <input
              type="password"
              id="senha"
              placeholder="Mínimo de 8 caracteres"
              required
              value={senha}
              onChange={(e) => setSenha(e.target.value)}
            />
          </div>

          <button type="submit">
            Criar conta
          </button>

        </form>

        <p>
          Já possui uma conta?{' '}
          <Link to="/login">
            Fazer login
          </Link>
        </p>

        {mensagem.texto && (
          <div className={`mensagem ${mensagem.tipo}`}>
            {mensagem.texto}
          </div>
        )}

      </div>
    </div>
  );
}

export default Register;