/**
 * Quick test script to verify the region-profiles API endpoint
 * Run with: node test_region_profiles_api.js
 */

const https = require('https');

const url = 'https://era-bot-group3-production.up.railway.app/api/region-profiles';

console.log('Testing region-profiles API endpoint...');
console.log(`URL: ${url}\n`);

https.get(url, (res) => {
  let data = '';

  res.on('data', (chunk) => {
    data += chunk;
  });

  res.on('end', () => {
    if (res.statusCode === 200) {
      try {
        const json = JSON.parse(data);
        const regions = json.regions || [];
        
        console.log('✅ API Response Successful!');
        console.log(`\nTotal Regions: ${regions.length}\n`);
        
        if (regions.length > 0) {
          console.log('Region Summary:');
          console.log('─'.repeat(80));
          regions.forEach((region, index) => {
            console.log(`\n${index + 1}. ${region.disco_name}`);
            console.log(`   ID: ${region.id}`);
            console.log(`   States: ${Array.isArray(region.states) ? region.states.join(', ') : 'N/A'}`);
            console.log(`   Avg Offtake: ${region.avg_offtake_mwh_per_hour?.toFixed(2) || 'N/A'} MWh/h`);
            console.log(`   Avg Available PCC: ${region.avg_available_pcc_mwh_per_hour?.toFixed(2) || 'N/A'} MWh/h`);
            console.log(`   Utilization: ${region.utilisation_percent?.toFixed(2) || 'N/A'}%`);
            console.log(`   Estimated Daily: ${region.estimated_daily_mwh?.toFixed(2) || 'N/A'} MWh`);
            console.log(`   Full Load Hours: ${region.estimated_full_load_hours?.toFixed(2) || 'N/A'} hours`);
            if (region.schedule_template && Array.isArray(region.schedule_template)) {
              console.log(`   Schedule Blocks: ${region.schedule_template.length}`);
            }
          });
          console.log('\n' + '─'.repeat(80));
          console.log(`\n✅ Total: ${regions.length} region profiles loaded successfully`);
        } else {
          console.log('⚠️  No regions found in response');
        }
      } catch (error) {
        console.error('❌ Error parsing JSON:', error.message);
        console.log('Raw response:', data);
      }
    } else {
      console.error(`❌ API Error: Status ${res.statusCode}`);
      console.log('Response:', data);
    }
  });
}).on('error', (error) => {
  console.error('❌ Request Error:', error.message);
});

