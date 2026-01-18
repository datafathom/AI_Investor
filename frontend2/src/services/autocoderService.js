/**
 * autoCoderService.js
 * 
 * Simulates the AI "Stacker Agent" writing code in real-time.
 * Provides streams of characters to create a hacking/coding effect.
 */

const DEMO_SCRIPTS = [
    {
        id: 'module_alpha_v1',
        name: 'Generate Alpha_Vantage_Wrapper.py',
        description: 'Implementing robust error handling for API rate limits.',
        language: 'python',
        code: `class AlphaVantageWrapper:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://www.alphavantage.co/query"
        self.session = requests.Session()

    def get_intraday(self, symbol, interval='5min'):
        """
        Fetches intraday time series for a given symbol.
        Implements exponential backoff for rate limits.
        """
        params = {
            "function": "TIME_SERIES_INTRADAY",
            "symbol": symbol,
            "interval": interval,
            "apikey": self.api_key
        }
        
        try:
            # AI OPTIMIZATION: Using retries with jitter
            response = self._make_request(params)
            data = response.json()
            
            if "Error Message" in data:
                raise ValueError(f"API Error: {data['Error Message']}")
                
            return self._parse_timeseries(data)
            
        except Exception as e:
            self.logger.error(f"Failed to fetch {symbol}: {str(e)}")
            return None

    def _make_request(self, params, retries=3):
        for i in range(retries):
            resp = self.session.get(self.base_url, params=params)
            if resp.status_code == 200:
                return resp
            time.sleep(2 ** i) # Exponential backoff
            
    # AI NOTE: Automatically verified against pylint
`
    },
    {
        id: 'strategy_mom_v2',
        name: 'Optimize Momentum_Strategy.py',
        description: 'Refining signal generation with RSI and MACD confluence.',
        language: 'python',
        code: `class MomentumStrategy(BaseStrategy):
    def on_tick(self, tick):
        # AI-derived Logic: check for trend strength
        rsi = self.indicators.rsi(tick.symbol, period=14)
        macd, signal, hist = self.indicators.macd(tick.symbol)
        
        # BUY SIGNAL CONFIRMATION
        if rsi < 30 and macd > signal:
            risk_score = self.risk_manager.evaluate(tick.symbol)
            
            if risk_score > 0.7:
                self.logger.info(f"High risk trade skipped: {tick.symbol}")
                return
                
            qty = self.position_sizer.calc(self.portfolio.balance)
            self.broker.submit_order(tick.symbol, qty, 'BUY')
            
        # SELL SIGNAL (Take Profit)
        elif rsi > 70:
            self.broker.close_position(tick.symbol)

    # Unit Test created autonomously:
    # test_momentum_strategy.py passed (14/14 tests)
`
    }
];

class AutoCoderService {
    constructor() {
        this.currentTask = null;
    }

    getTasks() {
        return DEMO_SCRIPTS.map(s => ({
            id: s.id,
            name: s.name,
            description: s.description
        }));
    }

    async streamCode(taskId, onChar, onComplete) {
        const script = DEMO_SCRIPTS.find(s => s.id === taskId);
        if (!script) return;

        this.currentTask = taskId;
        let index = 0;
        const code = script.code;

        // Simulate typing speed variation
        const typeChar = () => {
            if (index < code.length && this.currentTask === taskId) {
                onChar(code.substring(0, index + 1));
                index++;

                // Randomize typing speed (bursts and pauses)
                const delay = Math.random() > 0.9 ? 150 : Math.random() * 30 + 10;
                setTimeout(typeChar, delay);
            } else {
                if (this.currentTask === taskId) onComplete();
            }
        };

        typeChar();
    }

    stop() {
        this.currentTask = null;
    }
}

export const autoCoderService = new AutoCoderService();
export default autoCoderService;
